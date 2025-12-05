import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../test/test-utils';
import userEvent from '@testing-library/user-event';
import RegisterPage from './RegisterPage';
import { authService } from '../services/authService';

// Mock the authService
vi.mock('../services/authService', () => ({
  authService: {
    register: vi.fn(),
  },
}));

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('RegisterPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render registration form with all fields', () => {
    render(<RegisterPage />);

    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getAllByLabelText(/password/i).length).toBeGreaterThanOrEqual(2);
    expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
  });

  it('should render OAuth buttons', () => {
    render(<RegisterPage />);

    expect(screen.getByRole('button', { name: /github/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /google/i })).toBeInTheDocument();
  });

  it('should show validation error for empty name', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    const submitButton = screen.getByRole('button', { name: /create account/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short name', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/full name/i), 'A');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/name must be at least 2 characters/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for invalid email', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/email address/i), 'invalid-email');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
    });
  });

  it('should show validation error for short password', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'short');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/password must be at least 12 characters/i)).toBeInTheDocument();
    });
  });

  it('should show validation error when passwords do not match', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'ValidPassword123!');
    await user.type(passwordFields[1], 'DifferentPassword123!');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/passwords do not match/i)).toBeInTheDocument();
    });
  });

  it('should display password strength indicator when typing password', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'Weak1!');

    await waitFor(() => {
      expect(screen.getByText(/weak|fair|good/i)).toBeInTheDocument();
    });
  });

  it('should toggle password visibility', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    const passwordFields = screen.getAllByLabelText(/password/i);
    const passwordInput = passwordFields[0] as HTMLInputElement;
    expect(passwordInput.type).toBe('password');

    const toggleButtons = screen.getAllByLabelText(/toggle.*password visibility/i);
    await user.click(toggleButtons[0]);

    expect(passwordInput.type).toBe('text');

    await user.click(toggleButtons[0]);
    expect(passwordInput.type).toBe('password');
  });

  it('should submit form with valid data', async () => {
    const user = userEvent.setup();
    const mockResponse = {
      user: { id: '1', email: 'test@example.com', name: 'Test User' },
      token: 'mock-token',
    };

    vi.mocked(authService.register).mockResolvedValue(mockResponse);

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/full name/i), 'Test User');
    await user.type(screen.getByLabelText(/email address/i), 'test@example.com');

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'ValidPassword123!');
    await user.type(passwordFields[1], 'ValidPassword123!');

    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(authService.register).toHaveBeenCalledWith({
        name: 'Test User',
        email: 'test@example.com',
        password: 'ValidPassword123!',
      });
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('should show error message on registration failure', async () => {
    const user = userEvent.setup();
    vi.mocked(authService.register).mockRejectedValue({
      response: { data: { message: 'Email already exists' } },
    });

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/full name/i), 'Test User');
    await user.type(screen.getByLabelText(/email address/i), 'test@example.com');

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'ValidPassword123!');
    await user.type(passwordFields[1], 'ValidPassword123!');

    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/email already exists/i)).toBeInTheDocument();
    });
  });

  it('should disable form fields while loading', async () => {
    const user = userEvent.setup();
    vi.mocked(authService.register).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/full name/i), 'Test User');
    await user.type(screen.getByLabelText(/email address/i), 'test@example.com');

    const passwordFields = screen.getAllByLabelText(/password/i);
    await user.type(passwordFields[0], 'ValidPassword123!');
    await user.type(passwordFields[1], 'ValidPassword123!');

    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /creating account/i })).toBeDisabled();
    });
  });

  it('should have a link to login page', () => {
    render(<RegisterPage />);

    const loginLink = screen.getByRole('link', { name: /sign in/i });
    expect(loginLink).toBeInTheDocument();
    expect(loginLink).toHaveAttribute('href', '/login');
  });

  it('should clear field error when user starts typing', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    // Trigger validation error
    await user.click(screen.getByRole('button', { name: /create account/i }));
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });

    // Start typing in name field
    await user.type(screen.getByLabelText(/full name/i), 'T');

    // Error should be cleared
    await waitFor(() => {
      expect(screen.queryByText(/name is required/i)).not.toBeInTheDocument();
    });
  });
});
