import React, { useState, useEffect } from 'react';
import { Card, Button, Table, Input, Select, message, Space, Modal, Form } from 'antd';
import { ReloadOutlined, PlusOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';

const { Option } = Select;


interface Connection {
  id: string;
  name: string;
  host: string;
  port: number;
  type: string;
  status: string;
  lastConnected: string;
}

const Connect: React.FC = () => {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingConnection, setEditingConnection] = useState<Connection | null>(null);
  const [form] = Form.useForm();

  // 获取连接列表
  const fetchConnections = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取连接列表
      // 暂时使用模拟数据
      const mockConnections: Connection[] = [
        {
          id: '1',
          name: 'Localhost Connection',
          host: '127.0.0.1',
          port: 4444,
          type: 'TCP',
          status: 'connected',
          lastConnected: '2026-03-31 10:00:00'
        },
        {
          id: '2',
          name: 'Remote Server',
          host: '192.168.1.100',
          port: 5555,
          type: 'HTTPS',
          status: 'disconnected',
          lastConnected: '2026-03-30 15:30:00'
        }
      ];
      setConnections(mockConnections);
      message.success('获取连接列表成功');
    } catch (error) {
      console.error('Error fetching connections:', error);
      message.error('获取连接列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 连接到目标
  const handleConnect = async (connection: Connection) => {
    try {
      // 这里应该调用WebSocket服务连接到目标
      message.success(`正在连接到 ${connection.name}...`);
      // 模拟连接成功
      setTimeout(() => {
        message.success(`成功连接到 ${connection.name}`);
        setConnections(connections.map(conn => 
          conn.id === connection.id ? { ...conn, status: 'connected' } : conn
        ));
      }, 1000);
    } catch (error) {
      console.error('Error connecting:', error);
      message.error('连接失败');
    }
  };

  // 断开连接
  const handleDisconnect = async (connection: Connection) => {
    try {
      // 这里应该调用WebSocket服务断开连接
      message.success(`正在断开与 ${connection.name} 的连接...`);
      // 模拟断开成功
      setTimeout(() => {
        message.success(`成功断开与 ${connection.name} 的连接`);
        setConnections(connections.map(conn => 
          conn.id === connection.id ? { ...conn, status: 'disconnected' } : conn
        ));
      }, 1000);
    } catch (error) {
      console.error('Error disconnecting:', error);
      message.error('断开连接失败');
    }
  };

  // 删除连接
  const handleDelete = async (id: string) => {
    try {
      // 这里应该调用WebSocket服务删除连接
      setConnections(connections.filter(conn => conn.id !== id));
      message.success('删除连接成功');
    } catch (error) {
      console.error('Error deleting connection:', error);
      message.error('删除连接失败');
    }
  };

  // 编辑连接
  const handleEdit = (connection: Connection) => {
    setEditingConnection(connection);
    form.setFieldsValue(connection);
    setModalVisible(true);
  };

  // 添加连接
  const handleAdd = () => {
    setEditingConnection(null);
    form.resetFields();
    setModalVisible(true);
  };

  // 保存连接
  const handleSave = async (values: any) => {
    try {
      // 这里应该调用WebSocket服务保存连接
      if (editingConnection) {
        // 更新现有连接
        setConnections(connections.map(conn => 
          conn.id === editingConnection.id ? { ...conn, ...values } : conn
        ));
        message.success('更新连接成功');
      } else {
        // 添加新连接
        const newConnection: Connection = {
          id: (connections.length + 1).toString(),
          ...values,
          status: 'disconnected',
          lastConnected: new Date().toISOString().replace('T', ' ').substring(0, 19)
        };
        setConnections([...connections, newConnection]);
        message.success('添加连接成功');
      }
      setModalVisible(false);
    } catch (error) {
      console.error('Error saving connection:', error);
      message.error('保存连接失败');
    }
  };

  useEffect(() => {
    fetchConnections();
  }, []);

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '主机',
      dataIndex: 'host',
      key: 'host',
    },
    {
      title: '端口',
      dataIndex: 'port',
      key: 'port',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <span style={{
          color: status === 'connected' ? '#52c41a' : '#ff4d4f'
        }}>
          {status === 'connected' ? '已连接' : '未连接'}
        </span>
      ),
    },
    {
      title: '最后连接时间',
      dataIndex: 'lastConnected',
      key: 'lastConnected',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Connection) => (
        <Space size="middle">
          {record.status === 'disconnected' ? (
            <Button 
              type="primary" 
              size="small" 
              onClick={() => handleConnect(record)}
            >
              连接
            </Button>
          ) : (
            <Button 
              danger 
              size="small" 
              onClick={() => handleDisconnect(record)}
            >
              断开
            </Button>
          )}
          <Button 
            icon={<EditOutlined />} 
            size="small" 
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button 
            danger 
            icon={<DeleteOutlined />} 
            size="small" 
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="连接管理" 
        extra={
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={fetchConnections}
              loading={loading}
            >
              刷新
            </Button>
            <Button 
              type="primary" 
              icon={<PlusOutlined />} 
              onClick={handleAdd}
            >
              添加连接
            </Button>
          </Space>
        }
      >
        <Table 
          columns={columns} 
          dataSource={connections} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingConnection ? '编辑连接' : '添加连接'}
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => setModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
        >
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入连接名称' }]}
          >
            <Input placeholder="请输入连接名称" />
          </Form.Item>
          <Form.Item
            name="host"
            label="主机"
            rules={[{ required: true, message: '请输入主机地址' }]}
          >
            <Input placeholder="请输入主机地址" />
          </Form.Item>
          <Form.Item
            name="port"
            label="端口"
            rules={[{ required: true, message: '请输入端口号' }]}
          >
            <Input type="number" placeholder="请输入端口号" />
          </Form.Item>
          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择连接类型' }]}
          >
            <Select placeholder="请选择连接类型">
              <Option value="TCP">TCP</Option>
              <Option value="HTTPS">HTTPS</Option>
              <Option value="DNS">DNS</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Connect;