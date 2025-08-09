
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import WalletConnect from './WalletConnect';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import MenuIcon from '@mui/icons-material/Menu';
import BarChartIcon from '@mui/icons-material/BarChart';
import DescriptionIcon from '@mui/icons-material/Description';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import GroupsIcon from '@mui/icons-material/Groups';
import CloseIcon from '@mui/icons-material/Close';




import type { ReactNode, FC } from 'react';
type LayoutProps = {
  children: ReactNode;
};

const navigation = [
  { name: 'Dashboard', href: '/', icon: <BarChartIcon /> },
  { name: 'Proposal Analysis', href: '/proposals', icon: <DescriptionIcon /> },
  { name: 'Treasury Analysis', href: '/treasury', icon: <AccountBalanceIcon /> },
  { name: 'Governance Metrics', href: '/governance', icon: <GroupsIcon /> },
];

const Layout: FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  // Permanent drawer (desktop)
  const permanentDrawer = (
    <Box className="layout-drawer">
      <Box className="layout-drawer-header">
        <Typography variant="h6" noWrap component="div" className="layout-drawer-title">
          AIDA
        </Typography>
      </Box>
      <Typography variant="caption" className="layout-drawer-version">v1.0.0</Typography>
      <Divider className="layout-drawer-divider" />
      <List>
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <ListItem key={item.name} disablePadding>
              <ListItemButton
                component={Link}
                to={item.href}
                selected={isActive}
                onClick={() => setMobileOpen(false)}
              >
                <ListItemIcon className="layout-drawer-icon">{item.icon}</ListItemIcon>
                <ListItemText primary={item.name} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
      <Box className="layout-drawer-grow" />
    </Box>
  );

  // Mobile drawer (temporary)
  const mobileDrawer = (
    <Box className="layout-drawer">
      <Box className="layout-drawer-header">
        <Typography variant="h6" noWrap component="div" className="layout-drawer-title">
          AIDA
        </Typography>
        <IconButton onClick={() => setMobileOpen(false)} className="layout-drawer-close">
          <CloseIcon />
        </IconButton>
      </Box>
      <Typography variant="caption" className="layout-drawer-version">v1.0.0</Typography>
      <Divider className="layout-drawer-divider" />
      <List>
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <ListItem key={item.name} disablePadding>
              <ListItemButton
                component={Link}
                to={item.href}
                selected={isActive}
                onClick={() => setMobileOpen(false)}
              >
                <ListItemIcon className="layout-drawer-icon">{item.icon}</ListItemIcon>
                <ListItemText primary={item.name} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
      <Box className="layout-drawer-grow" />
    </Box>
  );

  return (
    <Box className="layout-root">
      <AppBar position="fixed" className="layout-appbar" color="primary" elevation={1}>
        <Toolbar
          sx={{
            display: 'flex',
            alignItems: 'center',
            minHeight: 64,
            px: { xs: 2, sm: 3, md: 4 },
          }}
        >
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={() => setMobileOpen(true)}
            className="layout-appbar-menu"
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Typography variant="h6" noWrap component="div" className="layout-appbar-title">
              <span className="brand-full">AI-Driven DAO Analyst</span>
              <span className="brand-short">AIDA</span>
            </Typography>
            <Typography variant="caption" color="#e0e0e0" sx={{ display: { xs: 'none', sm: 'block' }, fontWeight: 400, lineHeight: 1, mt: 0.25 }}>
              Secure, non-custodial wallet connection
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', ml: { xs: 1, sm: 2 } }}>
            <WalletConnect />
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className="layout-drawer-permanent"
        open
        sx={{
          display: { xs: 'none', md: 'block' },
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: { md: '18vw', lg: '15vw', xl: '13vw' },
            minWidth: '12rem',
            maxWidth: '16.25rem',
            boxSizing: 'border-box',
            top: '4rem',
            height: 'calc(100% - 4rem)',
            transition: 'width 0.2s',
          },
        }}
      >
        {permanentDrawer}
      </Drawer>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        ModalProps={{ keepMounted: true }}
        className="layout-drawer-mobile"
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': {
            width: '75vw',
            minWidth: '12rem',
            maxWidth: '20rem',
            boxSizing: 'border-box',
          },
        }}
      >
        {mobileDrawer}
      </Drawer>
      <Box
        component="main"
        className="layout-main"
        sx={{
          flexGrow: 1,
          paddingTop: '4rem',
          marginLeft: { md: '18vw', lg: '15vw', xl: '13vw', xs: 0 },
          transition: 'margin-left 0.2s',
          background: '#f8fafc',
          minHeight: '100vh',
        }}
      >
        <Box
          className="layout-main-inner"
          sx={{
            px: { xs: 2, sm: 3, md: 4, lg: 5 },
            py: { xs: 2, sm: 3 },
            maxWidth: '90vw',
            margin: '0 auto',
            width: '100%',
            boxSizing: 'border-box',
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );

};

export default Layout;