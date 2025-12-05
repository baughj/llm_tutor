import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import apiClient from '../services/api';

type VerificationStatus = 'loading' | 'success' | 'error' | 'expired' | 'invalid';

function EmailVerificationPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<VerificationStatus>('loading');
  const [message, setMessage] = useState<string>('');
  const [resending, setResending] = useState(false);

  const token = searchParams.get('token');
  const email = searchParams.get('email');

  useEffect(() => {
    verifyEmail();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const verifyEmail = async () => {
    if (!token) {
      setStatus('invalid');
      setMessage('Invalid verification link. Please check your email and try again.');
      return;
    }

    try {
      const response = await apiClient.post('/auth/verify-email', { token });
      setStatus('success');
      setMessage(response.data.message || 'Your email has been successfully verified!');

      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err: any) {
      const errorData = err.response?.data;

      if (errorData?.code === 'TOKEN_EXPIRED') {
        setStatus('expired');
        setMessage('This verification link has expired. Please request a new one.');
      } else if (errorData?.code === 'ALREADY_VERIFIED') {
        setStatus('success');
        setMessage('Your email is already verified. You can now log in.');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } else {
        setStatus('error');
        setMessage(errorData?.message || 'Email verification failed. Please try again.');
      }
    }
  };

  const handleResendVerification = async () => {
    if (!email) {
      setMessage('Unable to resend verification. Email address not found.');
      return;
    }

    setResending(true);

    try {
      await apiClient.post('/auth/resend-verification', { email });
      setMessage('A new verification email has been sent. Please check your inbox.');
      setStatus('success');
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to resend verification email.';
      setMessage(errorMsg);
    } finally {
      setResending(false);
    }
  };

  const renderContent = () => {
    switch (status) {
      case 'loading':
        return (
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} sx={{ mb: 3 }} />
            <Typography variant="h5" gutterBottom>
              Verifying your email...
            </Typography>
            <Typography color="text.secondary">
              Please wait while we verify your email address
            </Typography>
          </Box>
        );

      case 'success':
        return (
          <Box sx={{ textAlign: 'center' }}>
            <CheckCircleOutlineIcon
              sx={{ fontSize: 80, color: 'success.main', mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              Email Verified!
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 3 }}>
              {message}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Redirecting to login page...
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/login')}
              sx={{ mt: 2 }}
            >
              Go to Login
            </Button>
          </Box>
        );

      case 'expired':
        return (
          <Box sx={{ textAlign: 'center' }}>
            <ErrorOutlineIcon sx={{ fontSize: 80, color: 'warning.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Link Expired
            </Typography>
            <Alert severity="warning" sx={{ mb: 3, textAlign: 'left' }}>
              {message}
            </Alert>
            {email && (
              <Button
                variant="contained"
                onClick={handleResendVerification}
                disabled={resending}
                fullWidth
              >
                {resending ? 'Sending...' : 'Resend Verification Email'}
              </Button>
            )}
            <Button
              variant="outlined"
              onClick={() => navigate('/register')}
              fullWidth
              sx={{ mt: 2 }}
            >
              Back to Registration
            </Button>
          </Box>
        );

      case 'error':
      case 'invalid':
        return (
          <Box sx={{ textAlign: 'center' }}>
            <ErrorOutlineIcon sx={{ fontSize: 80, color: 'error.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Verification Failed
            </Typography>
            <Alert severity="error" sx={{ mb: 3, textAlign: 'left' }}>
              {message}
            </Alert>
            {email && status === 'error' && (
              <Button
                variant="contained"
                onClick={handleResendVerification}
                disabled={resending}
                fullWidth
                sx={{ mb: 2 }}
              >
                {resending ? 'Sending...' : 'Resend Verification Email'}
              </Button>
            )}
            <Button
              variant="outlined"
              onClick={() => navigate('/register')}
              fullWidth
            >
              Back to Registration
            </Button>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          py: 4,
        }}
      >
        <Paper elevation={3} sx={{ p: { xs: 3, sm: 4 }, width: '100%' }}>
          {renderContent()}
        </Paper>
      </Box>
    </Container>
  );
}

export default EmailVerificationPage;
