#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import {
  connect,
  JetStreamClient,
  JetStreamManager,
  StreamConfig,
  RetentionPolicy,
  StorageType,
  AckPolicy,
  DeliverPolicy,
  ReplayPolicy
} from "nats";

// Channel definitions
const CHANNELS = {
  roadmap: {
    name: "roadmap",
    description: "Discussion about project roadmap and planning",
    stream: "CHAT_ROADMAP",
    subject: "chat.roadmap",
  },
  "parallel-work": {
    name: "parallel-work",
    description: "Coordination for parallel work among agents",
    stream: "CHAT_PARALLEL_WORK",
    subject: "chat.parallel-work",
  },
  errors: {
    name: "errors",
    description: "Error reporting and troubleshooting",
    stream: "CHAT_ERRORS",
    subject: "chat.errors",
  },
};

// Server state
let agentHandle: string | null = null;
let natsConnection: any = null;
let jetStreamClient: JetStreamClient | null = null;
let jetStreamManager: JetStreamManager | null = null;

// Initialize NATS connection
async function initializeNATS() {
  if (natsConnection) return;

  try {
    // Connect to NATS (assumes NATS server running on localhost:4222)
    natsConnection = await connect({
      servers: ["localhost:4222"],
    });

    console.error("Connected to NATS");

    // Get JetStream client and manager
    jetStreamClient = natsConnection.jetstream();
    jetStreamManager = await natsConnection.jetstreamManager();

    // Create streams for each channel
    for (const channel of Object.values(CHANNELS)) {
      try {
        const streamConfig: Partial<StreamConfig> = {
          name: channel.stream,
          subjects: [channel.subject],
          retention: RetentionPolicy.Limits,
          max_msgs: 10000,
          max_bytes: 10485760, // 10MB
          max_age: 86400000000000, // 24 hours in nanoseconds
          storage: StorageType.File,
          num_replicas: 1,
        };

        await jetStreamManager!.streams.add(streamConfig);
        console.error(`Created stream: ${channel.stream}`);
      } catch (err: any) {
        if (err.message?.includes("already in use")) {
          console.error(`Stream ${channel.stream} already exists`);
        } else {
          console.error(`Error creating stream ${channel.stream}:`, err);
        }
      }
    }
  } catch (err) {
    console.error("Failed to connect to NATS:", err);
    throw new Error("NATS connection failed. Make sure NATS server with JetStream is running on localhost:4222");
  }
}

// MCP Server
const server = new Server(
  {
    name: "nats-chat",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
const tools: Tool[] = [
  {
    name: "set_handle",
    description: "Set your agent handle/username for the chat. This identifies you in all messages.",
    inputSchema: {
      type: "object",
      properties: {
        handle: {
          type: "string",
          description: "Your agent handle/username (e.g., 'project-manager', 'business-analyst')",
        },
      },
      required: ["handle"],
    },
  },
  {
    name: "list_channels",
    description: "List all available chat channels",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "send_message",
    description: "Send a message to a channel",
    inputSchema: {
      type: "object",
      properties: {
        channel: {
          type: "string",
          description: "Channel name (roadmap, parallel-work, or errors)",
          enum: ["roadmap", "parallel-work", "errors"],
        },
        message: {
          type: "string",
          description: "The message to send",
        },
      },
      required: ["channel", "message"],
    },
  },
  {
    name: "read_messages",
    description: "Read recent messages from a channel",
    inputSchema: {
      type: "object",
      properties: {
        channel: {
          type: "string",
          description: "Channel name (roadmap, parallel-work, or errors)",
          enum: ["roadmap", "parallel-work", "errors"],
        },
        limit: {
          type: "number",
          description: "Maximum number of messages to retrieve (default: 50)",
          default: 50,
        },
      },
      required: ["channel"],
    },
  },
  {
    name: "get_my_handle",
    description: "Get your current agent handle",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    await initializeNATS();

    switch (name) {
      case "set_handle": {
        const { handle } = args as { handle: string };
        agentHandle = handle;
        return {
          content: [
            {
              type: "text",
              text: `Handle set to: ${handle}\nYou can now send messages to channels!`,
            },
          ],
        };
      }

      case "get_my_handle": {
        if (!agentHandle) {
          return {
            content: [
              {
                type: "text",
                text: "No handle set. Use set_handle tool to choose your agent handle.",
              },
            ],
          };
        }
        return {
          content: [
            {
              type: "text",
              text: `Your current handle: ${agentHandle}`,
            },
          ],
        };
      }

      case "list_channels": {
        const channelList = Object.values(CHANNELS)
          .map((ch) => `- **${ch.name}**: ${ch.description}`)
          .join("\n");
        return {
          content: [
            {
              type: "text",
              text: `Available channels:\n${channelList}`,
            },
          ],
        };
      }

      case "send_message": {
        if (!agentHandle) {
          return {
            content: [
              {
                type: "text",
                text: "Error: You must set a handle first using set_handle tool.",
              },
            ],
          };
        }

        const { channel, message } = args as { channel: string; message: string };
        const channelConfig = CHANNELS[channel as keyof typeof CHANNELS];

        if (!channelConfig) {
          throw new Error(`Invalid channel: ${channel}`);
        }

        if (!jetStreamClient) {
          throw new Error("JetStream client not initialized");
        }

        const payload = {
          handle: agentHandle,
          message,
          timestamp: new Date().toISOString(),
        };

        await jetStreamClient.publish(
          channelConfig.subject,
          JSON.stringify(payload)
        );

        return {
          content: [
            {
              type: "text",
              text: `Message sent to #${channel} by ${agentHandle}`,
            },
          ],
        };
      }

      case "read_messages": {
        const { channel, limit = 50 } = args as { channel: string; limit?: number };
        const channelConfig = CHANNELS[channel as keyof typeof CHANNELS];

        if (!channelConfig) {
          throw new Error(`Invalid channel: ${channel}`);
        }

        if (!jetStreamManager) {
          throw new Error("JetStream manager not initialized");
        }

        const messages: any[] = [];

        try {
          const stream = await jetStreamManager.streams.get(channelConfig.stream);
          const consumer = await jetStreamClient!.consumers.get(
            channelConfig.stream,
            channelConfig.stream + "_READER"
          ).catch(async () => {
            // Create consumer if it doesn't exist
            return await jetStreamClient!.consumers.get(
              channelConfig.stream,
              await (async () => {
                const consumerConfig = {
                  durable_name: channelConfig.stream + "_READER",
                  ack_policy: AckPolicy.Explicit,
                  deliver_policy: DeliverPolicy.All,
                  replay_policy: ReplayPolicy.Instant,
                };
                await jetStreamManager!.consumers.add(channelConfig.stream, consumerConfig);
                return channelConfig.stream + "_READER";
              })()
            );
          });

          const iter = await consumer.fetch({ max_messages: limit, expires: 5000 });

          for await (const msg of iter) {
            try {
              const payload = JSON.parse(msg.data.toString());
              messages.push(payload);
              msg.ack();
            } catch (err) {
              console.error("Error parsing message:", err);
            }
          }
        } catch (err: any) {
          if (err.message?.includes("no messages")) {
            // No messages in stream yet
            return {
              content: [
                {
                  type: "text",
                  text: `No messages in #${channel} yet.`,
                },
              ],
            };
          }
          throw err;
        }

        if (messages.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: `No messages in #${channel} yet.`,
              },
            ],
          };
        }

        const formattedMessages = messages
          .map(
            (msg) =>
              `[${msg.timestamp}] **${msg.handle}**: ${msg.message}`
          )
          .join("\n");

        return {
          content: [
            {
              type: "text",
              text: `Messages from #${channel}:\n\n${formattedMessages}`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function runServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("NATS Chat MCP Server running on stdio");
}

runServer().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
