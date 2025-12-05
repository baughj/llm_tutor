import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../test/test-utils';
import userEvent from '@testing-library/user-event';
import EmailVerificationPage from './EmailVerificationPage';
import apiClient from '../services/api';

// Mock apiClient
vi.mock('../services/api');

// Mock useNavigate and useSearchParams
const mockNavigate = vi.fn();
let mockSearchParams = new URLSearchParams('token=valid-token&email=test@example.com');

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useSearchParams: () => [mockSearchParams, vi.fn()],
  };
});

describe('EmailVerificationPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSearchParams = new URLSearchParams('token=valid-token&email=test@example.com');
  });

  it('should show loading state initially', () => {
    vi.mocked(apiClient.post).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<EmailVerificationPage />);

    expect(screen.getByText(/verifying your email/i)).toBeInTheDocument();
  });

  it('should call verify endpoint with token', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { message: 'Success' },
    });

    render(<EmailVerificationPage />);

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/verify-email', {
        token: 'valid-token',
      });
    });
  });

  it('should show success state after verification', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { message: 'Email verified successfully' },
    });

    render(<EmailVerificationPage />);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /email verified/i })).toBeInTheDocument();
    }, { timeout: 1000 });
  });

  it('should show "Go to Login" button on success', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { message: 'Success' },
    });

    render(<EmailVerificationPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /go to login/i })).toBeInTheDocument();
    }, { timeout: 1000 });
  });

  it('should navigate to login when button is clicked', async () => {
    const user = userEvent.setup();
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { message: 'Success' },
    });

    render(<EmailVerificationPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /go to login/i })).toBeInTheDocument();
    });

    await user.click(screen.getByRole('button', { name: /go to login/i }));
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });
});
