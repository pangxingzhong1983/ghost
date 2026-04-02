import React, { useState } from 'react';
import { Card, Form, Input, Button, Typography, message, Alert } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';

const { Title } = Typography;

const TestLogin: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  const handleLogin = async () => {
    console.log('Test login attempt started');
    try {
      // 验证表单
      const values = await form.validateFields();
      console.log('Form values:', values);
      
      setLoading(true);
      console.log('Setting loading to true');
      
      // 直接设置localStorage
      const mockToken = 'test-token-' + Date.now();
      localStorage.setItem('token', mockToken);
      const expiry = new Date();
      expiry.setHours(expiry.getHours() + 24);
      localStorage.setItem('tokenExpiry', expiry.toISOString());
      localStorage.setItem('user', values.username);
      
      console.log('localStorage after test login:', {
        token: localStorage.getItem('token'),
        tokenExpiry: localStorage.getItem('tokenExpiry'),
        user: localStorage.getItem('user')
      });
      
      message.success('测试登录成功');
      console.log('Test login success message shown');
      
      // 导航到dashboard
      console.log('Navigating to dashboard');
      window.location.href = '/dashboard';
      console.log('Navigation attempted');
    } catch (error) {
      console.error('Test login error:', error);
      message.error('登录失败，请检查用户名和密码');
    } finally {
      setLoading(false);
      console.log('Setting loading to false');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
      <Card style={{ width: 400 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Ghost WebUI - 测试登录</Title>
        
        <Alert 
          message="测试登录信息" 
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
              测试登录
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default TestLogin;