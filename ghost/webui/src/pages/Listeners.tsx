import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Form, Input, Select, Modal, message, Spin, Popconfirm } from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import websocketService from '../services/websocket';

const { Title } = Typography;
const { Option } = Select;

interface Listener {
  id: string;
  name: string;
  transport: string;
  address: string;
  port: string;
  status: 'active' | 'inactive';
  info: string;
}

const Listeners: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [listeners, setListeners] = useState<Listener[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingListener, setEditingListener] = useState<Listener | null>(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockListeners: Listener[] = [
    {
      id: '1',
      name: 'tcp443',
      transport: 'tcp',
      address: '0.0.0.0',
      port: '443',
      status: 'active',
      info: 'TCP listener on port 443',
    },
    {
      id: '2',
      name: 'http80',
      transport: 'http',
      address: '0.0.0.0',
      port: '80',
      status: 'active',
      info: 'HTTP listener on port 80',
    },
    {
      id: '3',
      name: 'dns53',
      transport: 'dns',
      address: '0.0.0.0',
      port: '53',
      status: 'inactive',
      info: 'DNS listener on port 53',
    },
  ];

  useEffect(() => {
    const fetchListeners = async () => {
      try {
        setLoading(true);
        // 检查WebSocket连接状态
        if (!websocketService.isConnected()) {
          await websocketService.connect();
        }
        // 获取监听器列表
        const listeners = await websocketService.getListeners();
        setListeners(listeners);
      } catch (error) {
        console.error('Error fetching listeners:', error);
        // 使用模拟数据作为fallback
        setListeners(mockListeners);
      } finally {
        setLoading(false);
      }
    };

    fetchListeners();

    // 每30秒刷新一次监听器列表
    const interval = setInterval(fetchListeners, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleAddListener = () => {
    setEditingListener(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditListener = (listener: Listener) => {
    setEditingListener(listener);
    form.setFieldsValue({
      name: listener.name,
      transport: listener.transport,
      address: listener.address,
      port: listener.port,
    });
    setModalVisible(true);
  };

  const handleSaveListener = async () => {
    try {
      const values = await form.validateFields();
      if (editingListener) {
        // 编辑现有监听器
        await websocketService.executeCommand('listener', ['update', editingListener.id, ...Object.values(values) as string[]]);
        setListeners(listeners.map(listener => 
          listener.id === editingListener.id ? { ...listener, ...values } : listener
        ));
        message.success('监听器已更新');
      } else {
        // 添加新监听器
        await websocketService.executeCommand('listener', ['add', values.name, values.transport, values.address, values.port]);
        const newListener: Listener = {
          id: (listeners.length + 1).toString(),
          ...values,
          status: 'inactive',
          info: `${values.transport} listener on port ${values.port}`,
        };
        setListeners([...listeners, newListener]);
        message.success('监听器已添加');
      }
      setModalVisible(false);
    } catch (error) {
      console.error('Error saving listener:', error);
      message.error('保存监听器失败');
    }
  };

  const handleDeleteListener = async (id: string) => {
    try {
      // 使用WebSocket服务删除监听器
      await websocketService.executeCommand('listener', ['remove', id]);
      setListeners(listeners.filter(listener => listener.id !== id));
      message.success('监听器已删除');
    } catch (error) {
      console.error('Error deleting listener:', error);
      message.error('删除监听器失败');
    }
  };

  const handleToggleStatus = async (id: string) => {
    try {
      const listener = listeners.find(l => l.id === id);
      if (!listener) return;

      // 使用WebSocket服务启动或停止监听器
      if (listener.status === 'active') {
        await websocketService.executeCommand('listener', ['stop', id]);
      } else {
        await websocketService.executeCommand('listener', ['start', id]);
      }

      setListeners(listeners.map(listener => 
        listener.id === id ? {
          ...listener,
          status: listener.status === 'active' ? 'inactive' : 'active'
        } : listener
      ));
      message.success('监听器状态已切换');
    } catch (error) {
      console.error('Error toggling listener status:', error);
      message.error('切换监听器状态失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '传输协议',
      dataIndex: 'transport',
      key: 'transport',
      render: (transport: string) => (
        <Tag color={transport === 'tcp' ? 'blue' : transport === 'http' ? 'green' : 'purple'}>
          {transport}
        </Tag>
      ),
    },
    {
      title: '地址',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: '端口',
      dataIndex: 'port',
      key: 'port',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        status === 'active' ? (
          <Tag color="green">
            <CheckCircleOutlined /> 活跃
          </Tag>
        ) : (
          <Tag color="red">
            <CloseCircleOutlined /> 非活跃
          </Tag>
        )
      ),
    },
    {
      title: '信息',
      dataIndex: 'info',
      key: 'info',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Listener) => (
        <Space size="middle">
          <Button 
            danger={record.status === 'active'}
            type={record.status === 'inactive' ? 'primary' : 'default'}
            size="small"
            onClick={() => handleToggleStatus(record.id)}
          >
            {record.status === 'active' ? '停止' : '启动'}
          </Button>
          <Button size="small" onClick={() => handleEditListener(record)}>
            <EditOutlined />
          </Button>
          <Popconfirm
            title="确定要删除此监听器吗？"
            onConfirm={() => handleDeleteListener(record.id)}
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
      <Title level={2}>监听管理</Title>
      
      <Card>
        <div style={{ marginBottom: 16, textAlign: 'right' }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddListener}>
            添加监听器
          </Button>
        </div>
        
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={listeners} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title={editingListener ? "编辑监听器" : "添加监听器"}
        open={modalVisible}
        onOk={handleSaveListener}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入监听器名称' }]}
          >
            <Input placeholder="监听器名称" />
          </Form.Item>
          <Form.Item
            name="transport"
            label="传输协议"
            rules={[{ required: true, message: '请选择传输协议' }]}
          >
            <Select placeholder="选择传输协议">
              <Option value="tcp">TCP</Option>
              <Option value="http">HTTP</Option>
              <Option value="https">HTTPS</Option>
              <Option value="dns">DNS</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="address"
            label="地址"
            rules={[{ required: true, message: '请输入监听地址' }]}
          >
            <Input placeholder="监听地址 (0.0.0.0 表示所有接口)" />
          </Form.Item>
          <Form.Item
            name="port"
            label="端口"
            rules={[{ required: true, message: '请输入监听端口' }]}
          >
            <Input placeholder="监听端口" type="number" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Listeners;