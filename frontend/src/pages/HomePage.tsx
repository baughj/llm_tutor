import { Box, Container, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          gap: 3,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to CodeMentor
        </Typography>
        <Typography variant="h5" color="text.secondary" gutterBottom>
          Your personalized LLM-powered coding tutor
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/register')}
          >
            Get Started
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/login')}
          >
            Login
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default HomePage;
