# Responsive Design Guide

## Breakpoints

The application uses Material-UI's default breakpoint system:

- **xs**: 0px - Extra small (mobile)
- **sm**: 600px - Small (tablets)
- **md**: 960px - Medium (small laptops)
- **lg**: 1280px - Large (desktops)
- **xl**: 1920px - Extra large (large desktops)

## Usage

### Using the useResponsive Hook

```typescript
import { useResponsive } from '../hooks/useResponsive';

function MyComponent() {
  const { isMobile, isTablet, isDesktop } = useResponsive();

  return (
    <Box>
      {isMobile && <MobileView />}
      {isDesktop && <DesktopView />}
    </Box>
  );
}
```

### Using MUI sx prop

```typescript
<Box
  sx={{
    flexDirection: { xs: 'column', md: 'row' },
    padding: { xs: 2, sm: 3, md: 4 },
    fontSize: { xs: '0.875rem', sm: '1rem' },
  }}
>
  Content
</Box>
```

### Using theme breakpoints

```typescript
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

function MyComponent() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return <Box>{isMobile ? 'Mobile' : 'Desktop'}</Box>;
}
```

## Best Practices

1. **Mobile-First Approach**: Design for mobile first, then enhance for larger screens
2. **Use MUI Container**: Wrap page content in Container component for consistent margins
3. **Responsive Typography**: Use MUI Typography variants that scale automatically
4. **Test All Breakpoints**: Verify layout works at all breakpoint boundaries
5. **Touch Targets**: Ensure buttons/links are at least 44x44px on mobile
6. **Accessible**: Maintain WCAG 2.1 AA accessibility standards across all screen sizes
