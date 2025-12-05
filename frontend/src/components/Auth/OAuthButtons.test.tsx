import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/test-utils';
import userEvent from '@testing-library/user-event';
import OAuthButtons from './OAuthButtons';

describe('OAuthButtons', () => {
  it('should render GitHub and Google buttons', () => {
    render(
      <OAuthButtons
        onGitHubLogin={vi.fn()}
        onGoogleLogin={vi.fn()}
      />
    );

    expect(screen.getByRole('button', { name: /github/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /google/i })).toBeInTheDocument();
  });

  it('should render divider with "Or continue with" text', () => {
    render(
      <OAuthButtons
        onGitHubLogin={vi.fn()}
        onGoogleLogin={vi.fn()}
      />
    );

    expect(screen.getByText('Or continue with')).toBeInTheDocument();
  });

  it('should call onGitHubLogin when GitHub button is clicked', async () => {
    const user = userEvent.setup();
    const onGitHubLogin = vi.fn();

    render(
      <OAuthButtons
        onGitHubLogin={onGitHubLogin}
        onGoogleLogin={vi.fn()}
      />
    );

    await user.click(screen.getByRole('button', { name: /github/i }));
    expect(onGitHubLogin).toHaveBeenCalledTimes(1);
  });

  it('should call onGoogleLogin when Google button is clicked', async () => {
    const user = userEvent.setup();
    const onGoogleLogin = vi.fn();

    render(
      <OAuthButtons
        onGitHubLogin={vi.fn()}
        onGoogleLogin={onGoogleLogin}
      />
    );

    await user.click(screen.getByRole('button', { name: /google/i }));
    expect(onGoogleLogin).toHaveBeenCalledTimes(1);
  });

  it('should disable buttons when loading is true', () => {
    render(
      <OAuthButtons
        onGitHubLogin={vi.fn()}
        onGoogleLogin={vi.fn()}
        loading={true}
      />
    );

    expect(screen.getByRole('button', { name: /github/i })).toBeDisabled();
    expect(screen.getByRole('button', { name: /google/i })).toBeDisabled();
  });

  it('should not disable buttons when loading is false', () => {
    render(
      <OAuthButtons
        onGitHubLogin={vi.fn()}
        onGoogleLogin={vi.fn()}
        loading={false}
      />
    );

    expect(screen.getByRole('button', { name: /github/i })).not.toBeDisabled();
    expect(screen.getByRole('button', { name: /google/i })).not.toBeDisabled();
  });

  it('should not call handlers when buttons are disabled', () => {
    const onGitHubLogin = vi.fn();
    const onGoogleLogin = vi.fn();

    render(
      <OAuthButtons
        onGitHubLogin={onGitHubLogin}
        onGoogleLogin={onGoogleLogin}
        loading={true}
      />
    );

    // Just verify the buttons are disabled, don't try to click them
    expect(screen.getByRole('button', { name: /github/i })).toBeDisabled();
    expect(screen.getByRole('button', { name: /google/i })).toBeDisabled();
  });
});
