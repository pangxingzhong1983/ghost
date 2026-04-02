import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import Layout from './components/Layout';
import Login from './pages/Login';
import TestLogin from './pages/TestLogin';
import Dashboard from './pages/Dashboard';
import Sessions from './pages/Sessions';
import Listeners from './pages/Listeners';
import Payloads from './pages/Payloads';
import Modules from './pages/Modules';
import Credentials from './pages/Credentials';
import Jobs from './pages/Jobs';
import FileManager from './pages/FileManager';
import Network from './pages/Network';
import Config from './pages/Config';
import Tags from './pages/Tags';
import DnsC2 from './pages/DnsC2';
import PythonConsole from './pages/PythonConsole';
import Connect from './pages/Connect';
import Exposed from './pages/Exposed';
import Logging from './pages/Logging';
import ScreenControl from './pages/ScreenControl';
import Keylogger from './pages/Keylogger';
import SystemInfo from './pages/SystemInfo';
import ProcessManager from './pages/ProcessManager';
import SecurityTools from './pages/SecurityTools';
import NetworkTools from './pages/NetworkTools';
import SystemTools from './pages/SystemTools';
import DataCollection from './pages/DataCollection';
import FileSystem from './pages/FileSystem';
import ExecutionTools from './pages/ExecutionTools';
import Utilities from './pages/Utilities';
import './App.css';

// 检查是否已登录
const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  console.log('Authentication check:', token ? 'Authenticated' : 'Not authenticated');
  return token !== null;
};

// 受保护的路由组件
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuth = isAuthenticated();
  console.log('ProtectedRoute check:', isAuth ? 'Allowed' : 'Redirecting to login');
  if (!isAuth) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/test-login" element={<TestLogin />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/sessions" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Sessions />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/listeners" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Listeners />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/payloads" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Payloads />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/modules" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Modules />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/credentials" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Credentials />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/jobs" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Jobs />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/file-manager" 
            element={
              <ProtectedRoute>
                <Layout>
                  <FileManager />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/network" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Network />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/config" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Config />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/tags" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Tags />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/dns-c2" 
            element={
              <ProtectedRoute>
                <Layout>
                  <DnsC2 />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/python" 
            element={
              <ProtectedRoute>
                <Layout>
                  <PythonConsole />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/connect" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Connect />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/exposed" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Exposed />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/logging" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Logging />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/screen-control" 
            element={
              <ProtectedRoute>
                <Layout>
                  <ScreenControl />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/keylogger" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Keylogger />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/system-info" 
            element={
              <ProtectedRoute>
                <Layout>
                  <SystemInfo />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/process-manager" 
            element={
              <ProtectedRoute>
                <Layout>
                  <ProcessManager />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/security-tools" 
            element={
              <ProtectedRoute>
                <Layout>
                  <SecurityTools />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/network-tools" 
            element={
              <ProtectedRoute>
                <Layout>
                  <NetworkTools />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/system-tools" 
            element={
              <ProtectedRoute>
                <Layout>
                  <SystemTools />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/data-collection" 
            element={
              <ProtectedRoute>
                <Layout>
                  <DataCollection />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/file-system" 
            element={
              <ProtectedRoute>
                <Layout>
                  <FileSystem />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/execution-tools" 
            element={
              <ProtectedRoute>
                <Layout>
                  <ExecutionTools />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/utilities" 
            element={
              <ProtectedRoute>
                <Layout>
                  <Utilities />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route 
            path="/" 
            element={
              <Navigate to="/login" replace />
            }
          />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </ConfigProvider>
  );
}

export default App;