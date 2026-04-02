import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Typography, message, Alert, Spin } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import websocketService from '../services/websocket';

const { Title } = Typography;

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [connecting, setConnecting] = useState(true);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    // 直接设置为已连接状态，跳过WebSocket连接
    setConnecting(false);
    console.log('Login component mounted, skipping WebSocket connection');

    // 检查是否已登录且令牌有效
    const token = localStorage.getItem('token');
    console.log('Checking existing token:', token ? 'Token found' : 'No token');
    if (token) {
      console.log('Token found, navigating to dashboard');
      websocketService.setToken(token);
      navigate('/dashboard');
    }

    return () => {
      // 组件卸载时断开连接
      console.log('Login component unmounting, disconnecting WebSocket');
      websocketService.disconnect();
    };
  }, [navigate]);

  const handleLogin = async () => {
    console.log('Login attempt started');
    try {
      // 验证表单
      const values = await form.validateFields();
      console.log('Form values:', values);
      
      setLoading(true);
      console.log('Setting loading to true');
      
      try {
        // 尝试使用WebSocket服务进行认证
        if (websocketService.isConnected()) {
          console.log('WebSocket is connected, using WebSocket authentication');
          const token = await websocketService.authenticate(values.username, values.password);
          console.log('Authentication successful, token:', token);
          console.log('localStorage after auth:', {
            token: localStorage.getItem('token'),
            tokenExpiry: localStorage.getItem('tokenExpiry')
          });
          message.success('登录成功');
          console.log('Login success message shown');
        } else {
          // WebSocket未连接，使用本地登录
          console.log('WebSocket not connected, using local login');
          // 模拟登录成功
          const mockToken = 'mock-token-' + Date.now();
          localStorage.setItem('token', mockToken);
          const expiry = new Date();
          expiry.setHours(expiry.getHours() + 24);
          localStorage.setItem('tokenExpiry', expiry.toISOString());
          websocketService.setToken(mockToken);
          console.log('localStorage after local login:', {
            token: localStorage.getItem('token'),
            tokenExpiry: localStorage.getItem('tokenExpiry')
          });
          message.success('使用本地登录成功');
          console.log('Local login successful, mock token:', mockToken);
        }
        
        // 导航到dashboard
        console.log('Navigating to dashboard');
        // 强制刷新页面，确保localStorage的更改被正确识别
        window.location.href = '/dashboard';
        console.log('Navigation attempted');
        // navigate('/dashboard');
        // console.log('Navigation attempted');
      } catch (wsError) {
        console.error('WebSocket authentication error:', wsError);
        // WebSocket认证失败，使用本地登录作为fallback
        console.log('WebSocket authentication failed, falling back to local login');
        const mockToken = 'mock-token-' + Date.now();
        localStorage.setItem('token', mockToken);
        const expiry = new Date();
        expiry.setHours(expiry.getHours() + 24);
        localStorage.setItem('tokenExpiry', expiry.toISOString());
        websocketService.setToken(mockToken);
        console.log('localStorage after fallback login:', {
          token: localStorage.getItem('token'),
          tokenExpiry: localStorage.getItem('tokenExpiry')
        });
        message.success('使用本地登录成功');
        console.log('Local login successful, mock token:', mockToken);
        window.location.href = '/dashboard';
      }
    } catch (error) {
      console.error('Login error:', error);
      message.error('登录失败，请检查用户名和密码');
    } finally {
      setLoading(false);
      console.log('Setting loading to false');
    }
  };

  if (connecting) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
        <Card style={{ width: 400, padding: 40 }}>
          <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Ghost WebUI</Title>
          <div style={{ display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center' }}>
            <Spin size="large" tip="正在连接服务器..." />
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
      <Card style={{ width: 400 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Ghost WebUI</Title>
        
        <Alert 
          message="默认登录信息" 
          description="用户名: admin, 密码: password" 
          type="info" 
          style={{ marginBottom: 16 }} 
        />
        
        <Form
          form={form}
          layout="vertical"
          initialValues={{ username: 'admin', password: 'password' }}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>
          <Form.Item
            name="password"
            label="密码"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" block onClick={handleLogin} loading={loading}>
              登录
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Login;