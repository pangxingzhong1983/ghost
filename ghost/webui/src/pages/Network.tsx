import React, { useState, useEffect } from 'react';
import { Card, Typography, Spin, Table, Button, Space, Tag, Form, Input, Select, message, Tabs } from 'antd';
import {
  DeleteOutlined,
  EditOutlined,
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

interface NetworkInterface {
  id: string;
  name: string;
  type: string;
  ip: string;
  subnet: string;
  gateway: string;
  status: 'up' | 'down';
}

interface Route {
  id: string;
  destination: string;
  gateway: string;
  interface: string;
  metric: string;
}

const Network: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [interfaces, setInterfaces] = useState<NetworkInterface[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [form] = Form.useForm();

  // 模拟数据
  const mockInterfaces: NetworkInterface[] = [
    {
      id: '1',
      name: 'eth0',
      type: 'ethernet',
      ip: '192.168.1.100',
      subnet: '255.255.255.0',
      gateway: '192.168.1.1',
      status: 'up',
    },
    {
      id: '2',
      name: 'wlan0',
      type: 'wireless',
      ip: '10.0.0.100',
      subnet: '255.255.255.0',
      gateway: '10.0.0.1',
      status: 'up',
    },
  ];

  const mockRoutes: Route[] = [
    {
      id: '1',
      destination: '0.0.0.0/0',
      gateway: '192.168.1.1',
      interface: 'eth0',
      metric: '100',
    },
    {
      id: '2',
      destination: '192.168.1.0/24',
      gateway: '0.0.0.0',
      interface: 'eth0',
      metric: '0',
    },
  ];

  useEffect(() => {
    // 模拟加载数据
    setTimeout(() => {
      setInterfaces(mockInterfaces);
      setRoutes(mockRoutes);
      setLoading(false);
    }, 1000);
  }, []);

  const handleInterfaceUpDown = (id: string) => {
    setInterfaces(interfaces.map(intf => 
      intf.id === id ? {
        ...intf,
        status: intf.status === 'up' ? 'down' : 'up'
      } : intf
    ));
    message.success('网络接口状态已切换');
  };

  const handleAddRoute = () => {
    form.validateFields().then(() => {
      // 模拟添加路由
      message.success('路由已添加');
      form.resetFields();
    });
  };

  const handleDeleteRoute = (id: string) => {
    setRoutes(routes.filter(route => route.id !== id));
    message.success('路由已删除');
  };

  const interfaceColumns = [
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
        <Tag color={type === 'ethernet' ? 'blue' : 'green'}>
          {type}
        </Tag>
      ),
    },
    {
      title: 'IP地址',
      dataIndex: 'ip',
      key: 'ip',
    },
    {
      title: '子网掩码',
      dataIndex: 'subnet',
      key: 'subnet',
    },
    {
      title: '网关',
      dataIndex: 'gateway',
      key: 'gateway',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'up' ? 'green' : 'red'}>
          {status === 'up' ? '启用' : '禁用'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: NetworkInterface) => (
        <Space size="middle">
          <Button 
            danger={record.status === 'up'}
            type={record.status === 'down' ? 'primary' : 'default'}
            size="small"
            onClick={() => handleInterfaceUpDown(record.id)}
          >
            {record.status === 'up' ? '禁用' : '启用'}
          </Button>
          <Button size="small" onClick={() => {}}>
            <EditOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  const routeColumns = [
    {
      title: '目标',
      dataIndex: 'destination',
      key: 'destination',
    },
    {
      title: '网关',
      dataIndex: 'gateway',
      key: 'gateway',
    },
    {
      title: '接口',
      dataIndex: 'interface',
      key: 'interface',
    },
    {
      title: '度量',
      dataIndex: 'metric',
      key: 'metric',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Route) => (
        <Space size="middle">
          <Button size="small" onClick={() => {}}>
            <EditOutlined />
          </Button>
          <Button danger size="small" onClick={() => handleDeleteRoute(record.id)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>网络管理</Title>
      
      <Tabs defaultActiveKey="interfaces">
        <TabPane tab="网络接口" key="interfaces">
          <Card>
            {loading ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                <Spin size="large" />
              </div>
            ) : (
              <Table 
                columns={interfaceColumns} 
                dataSource={interfaces} 
                rowKey="id"
                pagination={{ pageSize: 10 }}
              />
            )}
          </Card>
        </TabPane>
        <TabPane tab="路由表" key="routes">
          <Card>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
              <Form form={form} layout="inline">
                <Form.Item name="destination" label="目标">
                  <Input placeholder="目标网络" />
                </Form.Item>
                <Form.Item name="gateway" label="网关">
                  <Input placeholder="网关地址" />
                </Form.Item>
                <Form.Item name="interface" label="接口">
                  <Select placeholder="选择接口">
                    {interfaces.map(intf => (
                      <Option key={intf.id} value={intf.name}>{intf.name}</Option>
                    ))}
                  </Select>
                </Form.Item>
                <Form.Item name="metric" label="度量">
                  <Input placeholder="度量值" type="number" />
                </Form.Item>
                <Form.Item>
                  <Button type="primary" onClick={handleAddRoute}>
                    添加路由
                  </Button>
                </Form.Item>
              </Form>
            </div>
            
            {loading ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                <Spin size="large" />
              </div>
            ) : (
              <Table 
                columns={routeColumns} 
                dataSource={routes} 
                rowKey="id"
                pagination={{ pageSize: 10 }}
              />
            )}
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default Network;