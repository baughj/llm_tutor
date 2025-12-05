import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/test-utils';
import PasswordStrengthIndicator from './PasswordStrengthIndicator';

describe('PasswordStrengthIndicator', () => {
  it('should not render when password is empty', () => {
    const { container } = render(<PasswordStrengthIndicator password="" />);
    expect(container.firstChild).toBeNull();
  });

  it('should show "Weak" for a short password', () => {
    render(<PasswordStrengthIndicator password="abc" />);
    expect(screen.getByText('Weak')).toBeInTheDocument();
  });

  it('should show "Fair" for password with only lowercase', () => {
    // 12+ chars (25) + lowercase (20) = 45 (Fair)
    render(<PasswordStrengthIndicator password="abcdefghijkl" />);
    expect(screen.getByText('Fair')).toBeInTheDocument();
  });

  it('should show "Good" for password with lowercase and uppercase', () => {
    // 12+ chars (25) + uppercase (20) + lowercase (20) = 65 (Good)
    render(<PasswordStrengthIndicator password="Abcdefghijkl" />);
    expect(screen.getByText('Good')).toBeInTheDocument();
  });

  it('should show "Strong" for password with lowercase, uppercase, and numbers', () => {
    // 12+ chars (25) + uppercase (20) + lowercase (20) + number (20) = 85 (Strong)
    render(<PasswordStrengthIndicator password="Abcdefghijk1" />);
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });

  it('should show "Strong" for password meeting all requirements', () => {
    render(<PasswordStrengthIndicator password="Abcdefgh123!" />);
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });

  it('should display helper text with password requirements', () => {
    render(<PasswordStrengthIndicator password="test" />);
    expect(
      screen.getByText('Use 12+ characters with mixed case, numbers, and symbols')
    ).toBeInTheDocument();
  });

  it('should give higher score for longer passwords', () => {
    const { rerender } = render(<PasswordStrengthIndicator password="Abc123!" />);
    // Abc123! has all character types but is only 7 characters = 75 points = Good
    expect(screen.getByText('Good')).toBeInTheDocument();

    rerender(<PasswordStrengthIndicator password="Abc123!Abc123!" />);
    // Abc123!Abc123! is 14 characters with all types = 100 points = Strong
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });

  it('should handle special characters correctly', () => {
    render(<PasswordStrengthIndicator password="Abc123!@#$%^" />);
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });

  it('should update when password changes', () => {
    const { rerender } = render(<PasswordStrengthIndicator password="weak" />);
    expect(screen.getByText('Weak')).toBeInTheDocument();

    rerender(<PasswordStrengthIndicator password="StrongP@ssw0rd!" />);
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });
});
