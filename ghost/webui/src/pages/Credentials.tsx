import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Form, Input, Select, Modal, message, Spin, Popconfirm } from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  EyeOutlined,
  EyeInvisibleOutlined,
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

interface Credential {
  id: string;
  username: string;
  password: string;
  domain: string;
  type: string;
  source: string;
  host: string;
  note: string;
}

const Credentials: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [credentials, setCredentials] = useState<Credential[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCredential, setEditingCredential] = useState<Credential | null>(null);
  const [form] = Form.useForm();
  const [showPassword, setShowPassword] = useState(false);

  // 模拟数据
  const mockCredentials: Credential[] = [
    {
      id: '1',
      username: 'Administrator',
      password: 'Password123',
      domain: 'DOMAIN',
      type: 'windows',
      source: 'mimikatz',
      host: '192.168.1.100',
      note: 'Local administrator',
    },
    {
      id: '2',
      username: 'root',
      password: 'toor',
      domain: '',
      type: 'linux',
      source: 'ssh',
      host: '192.168.1.101',
      note: 'Root user',
    },
    {
      id: '3',
      username: 'user',
      password: 'user123',
      domain: '',
      type: 'macos',
      source: 'keychain',
      host: '192.168.1.102',
      note: 'Standard user',
    },
  ];

  useEffect(() => {
    // 模拟加载数据
    setTimeout(() => {
      setCredentials(mockCredentials);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAddCredential = () => {
    setEditingCredential(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditCredential = (credential: Credential) => {
    setEditingCredential(credential);
    form.setFieldsValue(credential);
    setModalVisible(true);
  };

  const handleSaveCredential = () => {
    form.validateFields().then(values => {
      if (editingCredential) {
        // 编辑现有凭证
        setCredentials(credentials.map(credential => 
          credential.id === editingCredential.id ? { ...credential, ...values } : credential
        ));
        message.success('凭证已更新');
      } else {
        // 添加新凭证
        const newCredential: Credential = {
          id: (credentials.length + 1).toString(),
          ...values,
        };
        setCredentials([...credentials, newCredential]);
        message.success('凭证已添加');
      }
      setModalVisible(false);
    });
  };

  const handleDeleteCredential = (id: string) => {
    setCredentials(credentials.filter(credential => credential.id !== id));
    message.success('凭证已删除');
  };

  const columns = [
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: '密码',
      dataIndex: 'password',
      key: 'password',
      render: (password: string) => (
        <Space>
          {showPassword ? password : '••••••••'}
          <Button
            icon={showPassword ? <EyeInvisibleOutlined /> : <EyeOutlined />}
            size="small"
            onClick={() => setShowPassword(!showPassword)}
          />
        </Space>
      ),
    },
    {
      title: '域',
      dataIndex: 'domain',
      key: 'domain',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={type === 'windows' ? 'blue' : type === 'linux' ? 'green' : 'purple'}>
          {type}
        </Tag>
      ),
    },
    {
      title: '来源',
      dataIndex: 'source',
      key: 'source',
    },
    {
      title: '主机',
      dataIndex: 'host',
      key: 'host',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Credential) => (
        <Space size="middle">
          <Button size="small" onClick={() => handleEditCredential(record)}>
            <EditOutlined />
          </Button>
          <Popconfirm
            title="确定要删除此凭证吗？"
            onConfirm={() => handleDeleteCredential(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button danger size="small">
              <DeleteOutlined />
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>凭证管理</Title>
      
      <Card>
        <div style={{ marginBottom: 16, textAlign: 'right' }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddCredential}>
            添加凭证
          </Button>
        </div>
        
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={credentials} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title={editingCredential ? "编辑凭证" : "添加凭证"}
        open={modalVisible}
        onOk={handleSaveCredential}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input placeholder="用户名" />
          </Form.Item>
          <Form.Item
            name="password"
            label="密码"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password placeholder="密码" />
          </Form.Item>
          <Form.Item
            name="domain"
            label="域"
          >
            <Input placeholder="域 (可选)" />
          </Form.Item>
          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择类型' }]}
          >
            <Select placeholder="选择类型">
              <Option value="windows">Windows</Option>
              <Option value="linux">Linux</Option>
              <Option value="macos">macOS</Option>
              <Option value="other">Other</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="source"
            label="来源"
            rules={[{ required: true, message: '请输入来源' }]}
          >
            <Input placeholder="来源 (如 mimikatz, ssh 等)" />
          </Form.Item>
          <Form.Item
            name="host"
            label="主机"
            rules={[{ required: true, message: '请输入主机' }]}
          >
            <Input placeholder="主机 IP 或域名" />
          </Form.Item>
          <Form.Item
            name="note"
            label="备注"
          >
            <Input.TextArea placeholder="备注 (可选)" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Credentials;