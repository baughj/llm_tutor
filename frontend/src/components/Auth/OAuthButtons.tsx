import { Button, Stack, Divider, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import GoogleIcon from '@mui/icons-material/Google';

interface OAuthButtonsProps {
  onGitHubLogin: () => void;
  onGoogleLogin: () => void;
  loading?: boolean;
}

function OAuthButtons({ onGitHubLogin, onGoogleLogin, loading = false }: OAuthButtonsProps) {
  return (
    <>
      <Divider sx={{ my: 3 }}>
        <Typography variant="body2" color="text.secondary">
          Or continue with
        </Typography>
      </Divider>

      <Stack spacing={2}>
        <Button
          variant="outlined"
          startIcon={<GitHubIcon />}
          onClick={onGitHubLogin}
          disabled={loading}
          fullWidth
          sx={{
            borderColor: 'rgba(0, 0, 0, 0.23)',
            color: 'text.primary',
            '&:hover': {
              borderColor: 'rgba(0, 0, 0, 0.87)',
              backgroundColor: 'rgba(0, 0, 0, 0.04)',
            },
          }}
        >
          GitHub
        </Button>

        <Button
          variant="outlined"
          startIcon={<GoogleIcon />}
          onClick={onGoogleLogin}
          disabled={loading}
          fullWidth
          sx={{
            borderColor: 'rgba(0, 0, 0, 0.23)',
            color: 'text.primary',
            '&:hover': {
              borderColor: 'rgba(0, 0, 0, 0.87)',
              backgroundColor: 'rgba(0, 0, 0, 0.04)',
            },
          }}
        >
          Google
        </Button>
      </Stack>
    </>
  );
}

export default OAuthButtons;
