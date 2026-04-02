import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Form, Input, Select, Modal, message, Spin } from 'antd';
import {
  PlusOutlined,
  DownloadOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import websocketService from '../services/websocket';

const { Title } = Typography;
const { Option } = Select;

interface Payload {
  id: string;
  name: string;
  type: string;
  platform: string;
  arch: string;
  listener: string;
  status: 'generated' | 'expired' | 'used';
  created_at: string;
  expires_at: string;
  size: string;
}

const Payloads: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [payloads, setPayloads] = useState<Payload[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  // 模拟数据
  const mockPayloads: Payload[] = [
    {
      id: '1',
      name: 'Windows Reverse Shell',
      type: 'exe',
      platform: 'windows',
      arch: 'x64',
      listener: 'HTTP Listener',
      status: 'generated',
      created_at: '2026-03-30 14:00:00',
      expires_at: '2026-04-01 14:00:00',
      size: '1.2 MB',
    },
    {
      id: '2',
      name: 'Linux Reverse Shell',
      type: 'elf',
      platform: 'linux',
      arch: 'x64',
      listener: 'HTTPS Listener',
      status: 'used',
      created_at: '2026-03-30 13:30:00',
      expires_at: '2026-04-01 13:30:00',
      size: '800 KB',
    },
    {
      id: '3',
      name: 'MacOS Reverse Shell',
      type: 'macho',
      platform: 'macos',
      arch: 'x64',
      listener: 'HTTP Listener',
      status: 'expired',
      created_at: '2026-03-28 10:00:00',
      expires_at: '2026-03-29 10:00:00',
      size: '1.5 MB',
    },
  ];

  useEffect(() => {
    const fetchPayloads = async () => {
      try {
        setLoading(true);
        // 检查WebSocket连接状态
        if (!websocketService.isConnected()) {
          await websocketService.connect();
        }
        // 获取Payload列表
        const payloads = await websocketService.getPayloads();
        setPayloads(payloads);
      } catch (error) {
        console.error('Error fetching payloads:', error);
        // 使用模拟数据作为fallback
        setPayloads(mockPayloads);
      } finally {
        setLoading(false);
      }
    };

    fetchPayloads();

    // 每30秒刷新一次Payload列表
    const interval = setInterval(fetchPayloads, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleGeneratePayload = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      // 使用WebSocket服务生成Payload
      await websocketService.generatePayload({
        name: values.name,
        type: values.type,
        platform: values.platform,
        arch: values.arch,
        listener: values.listener,
        expiration: values.expiration
      });
      message.success('Payload生成成功');
      setModalVisible(false);
      form.resetFields();
      // 刷新Payload列表
      const payloads = await websocketService.getPayloads();
      setPayloads(payloads);
    } catch (error) {
      console.error('Error generating payload:', error);
      message.error('Payload生成失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPayload = async (id: string) => {
    try {
      // 使用WebSocket服务下载Payload
      await websocketService.executeCommand('payload', ['download', id]);
      message.success('Payload下载开始');
    } catch (error) {
      console.error('Error downloading payload:', error);
      message.error('Payload下载失败');
    }
  };

  const handleDeletePayload = async (id: string) => {
    try {
      // 使用WebSocket服务删除Payload
      await websocketService.executeCommand('payload', ['remove', id]);
      setPayloads(payloads.filter(payload => payload.id !== id));
      message.success('Payload已删除');
    } catch (error) {
      console.error('Error deleting payload:', error);
      message.error('Payload删除失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={type === 'exe' ? 'blue' : type === 'elf' ? 'green' : 'purple'}>
          {type}
        </Tag>
      ),
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
      render: (platform: string) => (
        <Tag color={platform === 'windows' ? 'blue' : platform === 'linux' ? 'green' : 'purple'}>
          {platform}
        </Tag>
      ),
    },
    {
      title: '架构',
      dataIndex: 'arch',
      key: 'arch',
      render: (arch: string) => (
        <Tag color={arch === 'x86' ? 'blue' : 'green'}>
          {arch}
        </Tag>
      ),
    },
    {
      title: '监听器',
      dataIndex: 'listener',
      key: 'listener',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = '';
        let text = '';
        switch (status) {
          case 'generated':
            color = 'green';
            text = '已生成';
            break;
          case 'used':
            color = 'blue';
            text = '已使用';
            break;
          case 'expired':
            color = 'red';
            text = '已过期';
            break;
          default:
            color = 'default';
            text = status;
        }
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '大小',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Payload) => (
        <Space size="middle">
          <Button size="small" icon={<DownloadOutlined />} onClick={() => handleDownloadPayload(record.id)}>
            下载
          </Button>
          <Button danger size="small" icon={<DeleteOutlined />} onClick={() => handleDeletePayload(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Payload管理</Title>
      
      <Card>
        <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'flex-end' }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
            生成Payload
          </Button>
        </div>
        
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={payloads} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title="生成Payload"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={[
          <Button key="cancel" onClick={() => setModalVisible(false)}>
            取消
          </Button>,
          <Button key="generate" type="primary" onClick={handleGeneratePayload} loading={loading}>
            生成
          </Button>,
        ]}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Payload名称"
            rules={[{ required: true, message: '请输入Payload名称' }]}
          >
            <Input placeholder="Payload名称" />
          </Form.Item>
          <Form.Item
            name="type"
            label="Payload类型"
            rules={[{ required: true, message: '请选择Payload类型' }]}
          >
            <Select placeholder="选择Payload类型">
              <Option value="exe">EXE</Option>
              <Option value="dll">DLL</Option>
              <Option value="powershell">PowerShell</Option>
              <Option value="elf">ELF</Option>
              <Option value="macho">Mach-O</Option>
              <Option value="python">Python</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="platform"
            label="目标平台"
            rules={[{ required: true, message: '请选择目标平台' }]}
          >
            <Select placeholder="选择目标平台">
              <Option value="windows">Windows</Option>
              <Option value="linux">Linux</Option>
              <Option value="macos">macOS</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="arch"
            label="架构"
            rules={[{ required: true, message: '请选择架构' }]}
          >
            <Select placeholder="选择架构">
              <Option value="x86">x86</Option>
              <Option value="x64">x64</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="listener"
            label="监听器"
            rules={[{ required: true, message: '请选择监听器' }]}
          >
            <Select placeholder="选择监听器">
              <Option value="HTTP Listener">HTTP Listener</Option>
              <Option value="HTTPS Listener">HTTPS Listener</Option>
              <Option value="TCP Listener">TCP Listener</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="expiration"
            label="过期时间"
            rules={[{ required: true, message: '请输入过期时间' }]}
          >
            <Input placeholder="过期时间 (小时)" type="number" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Payloads;