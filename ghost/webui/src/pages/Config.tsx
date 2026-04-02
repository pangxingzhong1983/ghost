import React, { useState } from 'react';
import { Card, Form, Input, Select, Switch, Button, Typography, message } from 'antd';
import {
  SaveOutlined,
  ReloadOutlined,
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const Config: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  // 模拟配置数据
  const defaultConfig = {
    server_port: '8080',
    ssl_enabled: false,
    ssl_cert: '',
    ssl_key: '',
    log_level: 'info',
    max_sessions: '100',
    session_timeout: '3600',
    auto_save: true,
  };

  const handleSaveConfig = () => {
    form.validateFields().then(() => {
      setLoading(true);
      // 模拟保存配置
      setTimeout(() => {
        message.success('配置已保存');
        setLoading(false);
      }, 1000);
    });
  };

  const handleResetConfig = () => {
    form.setFieldsValue(defaultConfig);
    message.info('配置已重置');
  };

  return (
    <div>
      <Title level={2}>配置管理</Title>
      
      <Card>
        <Form
          form={form}
          layout="vertical"
          initialValues={defaultConfig}
        >
          <Form.Item
            name="server_port"
            label="服务器端口"
            rules={[{ required: true, message: '请输入服务器端口' }]}
          >
            <Input placeholder="服务器端口" type="number" />
          </Form.Item>
          
          <Form.Item
            name="ssl_enabled"
            label="启用SSL"
          >
            <Switch />
          </Form.Item>
          
          <Form.Item
            name="ssl_cert"
            label="SSL证书路径"
          >
            <Input placeholder="SSL证书路径" />
          </Form.Item>
          
          <Form.Item
            name="ssl_key"
            label="SSL密钥路径"
          >
            <Input placeholder="SSL密钥路径" />
          </Form.Item>
          
          <Form.Item
            name="log_level"
            label="日志级别"
            rules={[{ required: true, message: '请选择日志级别' }]}
          >
            <Select placeholder="选择日志级别">
              <Option value="debug">Debug</Option>
              <Option value="info">Info</Option>
              <Option value="warn">Warn</Option>
              <Option value="error">Error</Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            name="max_sessions"
            label="最大会话数"
            rules={[{ required: true, message: '请输入最大会话数' }]}
          >
            <Input placeholder="最大会话数" type="number" />
          </Form.Item>
          
          <Form.Item
            name="session_timeout"
            label="会话超时(秒)"
            rules={[{ required: true, message: '请输入会话超时时间' }]}
          >
            <Input placeholder="会话超时时间" type="number" />
          </Form.Item>
          
          <Form.Item
            name="auto_save"
            label="自动保存配置"
          >
            <Switch />
          </Form.Item>
          
          <Form.Item>
            <div style={{ display: 'flex', gap: 16 }}>
              <Button type="primary" icon={<SaveOutlined />} onClick={handleSaveConfig} loading={loading}>
                保存配置
              </Button>
              <Button icon={<ReloadOutlined />} onClick={handleResetConfig}>
                重置
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Config;