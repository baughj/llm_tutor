import { Box, Container, Typography, Paper } from '@mui/material';

function DashboardPage() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
          <Typography color="text.secondary">
            Dashboard will be implemented in Work Stream D4
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}

export default DashboardPage;
