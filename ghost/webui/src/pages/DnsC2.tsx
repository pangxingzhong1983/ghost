import React, { useState } from 'react';
import { Card, Typography, Spin, Table, Button, Space, Tag, Form, Input, Select, message, Tabs, Alert, Modal } from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
} from '@ant-design/icons';

const { Title } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;

interface DnsRecord {
  id: string;
  type: string;
  name: string;
  value: string;
  ttl: string;
  status: 'active' | 'inactive';
}

const DnsC2: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [records, setRecords] = useState<DnsRecord[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRecord, setEditingRecord] = useState<DnsRecord | null>(null);
  const [form] = Form.useForm();
  const [dnsServerStatus, setDnsServerStatus] = useState<'running' | 'stopped'>('stopped');

  // 模拟数据
  const mockRecords: DnsRecord[] = [
    {
      id: '1',
      type: 'A',
      name: 'c2.example.com',
      value: '192.168.1.100',
      ttl: '300',
      status: 'active',
    },
    {
      id: '2',
      type: 'NS',
      name: 'c2.example.com',
      value: 'ns1.example.com',
      ttl: '3600',
      status: 'active',
    },
    {
      id: '3',
      type: 'TXT',
      name: 'data.c2.example.com',
      value: 'payload=123456',
      ttl: '60',
      status: 'active',
    },
  ];

  React.useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setRecords(mockRecords);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAddRecord = () => {
    setEditingRecord(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditRecord = (record: DnsRecord) => {
    setEditingRecord(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleSaveRecord = () => {
    form.validateFields().then(values => {
      if (editingRecord) {
        // 编辑现有记录
        setRecords(records.map(record => 
          record.id === editingRecord.id ? { ...record, ...values } : record
        ));
        message.success('DNS记录已更新');
      } else {
        // 添加新记录
        const newRecord: DnsRecord = {
          id: (records.length + 1).toString(),
          ...values,
          status: 'active',
        };
        setRecords([...records, newRecord]);
        message.success('DNS记录已添加');
      }
      setModalVisible(false);
    });
  };

  const handleDeleteRecord = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
    message.success('DNS记录已删除');
  };

  const handleToggleStatus = (id: string) => {
    setRecords(records.map(record => 
      record.id === id ? {
        ...record,
        status: record.status === 'active' ? 'inactive' : 'active'
      } : record
    ));
    message.success('DNS记录状态已切换');
  };

  const handleStartDnsServer = () => {
    setDnsServerStatus('running');
    message.success('DNS服务器已启动');
  };

  const handleStopDnsServer = () => {
    setDnsServerStatus('stopped');
    message.success('DNS服务器已停止');
  };

  const columns = [
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => <Tag>{type}</Tag>,
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '值',
      dataIndex: 'value',
      key: 'value',
    },
    {
      title: 'TTL',
      dataIndex: 'ttl',
      key: 'ttl',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '活跃' : '非活跃'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: DnsRecord) => (
        <Space size="middle">
          <Button 
            danger={record.status === 'active'}
            type={record.status === 'inactive' ? 'primary' : 'default'}
            size="small"
            onClick={() => handleToggleStatus(record.id)}
          >
            {record.status === 'active' ? '禁用' : '启用'}
          </Button>
          <Button size="small" onClick={() => handleEditRecord(record)}>
            <EditOutlined />
          </Button>
          <Button danger size="small" onClick={() => handleDeleteRecord(record.id)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>DNS C2管理</Title>
      
      <Tabs defaultActiveKey="records">
        <TabPane tab="DNS记录" key="records">
          <Card>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
              <Space>
                <Button 
                  danger={dnsServerStatus === 'running'}
                  type={dnsServerStatus === 'stopped' ? 'primary' : 'default'}
                  icon={dnsServerStatus === 'running' ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                  onClick={dnsServerStatus === 'running' ? handleStopDnsServer : handleStartDnsServer}
                >
                  {dnsServerStatus === 'running' ? '停止DNS服务器' : '启动DNS服务器'}
                </Button>
                <Tag color={dnsServerStatus === 'running' ? 'green' : 'red'}>
                  {dnsServerStatus === 'running' ? '运行中' : '已停止'}
                </Tag>
              </Space>
              <Button type="primary" icon={<PlusOutlined />} onClick={handleAddRecord}>
                添加DNS记录
              </Button>
            </div>
            
            {loading ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                <Spin size="large" />
              </div>
            ) : (
              <Table 
                columns={columns} 
                dataSource={records} 
                rowKey="id"
                pagination={{ pageSize: 10 }}
              />
            )}
          </Card>
        </TabPane>
        
        <TabPane tab="配置" key="config">
          <Card>
            <Form layout="vertical">
              <Form.Item
                label="DNS服务器地址"
                rules={[{ required: true, message: '请输入DNS服务器地址' }]}
              >
                <Input placeholder="例如: 0.0.0.0" />
              </Form.Item>
              <Form.Item
                label="DNS服务器端口"
                rules={[{ required: true, message: '请输入DNS服务器端口' }]}
              >
                <Input type="number" placeholder="例如: 53" />
              </Form.Item>
              <Form.Item
                label="域名"
                rules={[{ required: true, message: '请输入域名' }]}
              >
                <Input placeholder="例如: example.com" />
              </Form.Item>
              <Form.Item
                label="DNS解析器"
                rules={[{ required: true, message: '请输入DNS解析器' }]}
              >
                <Input placeholder="例如: 8.8.8.8" />
              </Form.Item>
              <Form.Item>
                <Button type="primary">保存配置</Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="统计" key="stats">
          <Card>
            <Alert message="DNS请求统计功能开发中" type="info" />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title={editingRecord ? "编辑DNS记录" : "添加DNS记录"}
        open={modalVisible}
        onOk={handleSaveRecord}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="type"
            label="记录类型"
            rules={[{ required: true, message: '请选择记录类型' }]}
          >
            <Select placeholder="选择记录类型">
              <Option value="A">A</Option>
              <Option value="AAAA">AAAA</Option>
              <Option value="NS">NS</Option>
              <Option value="CNAME">CNAME</Option>
              <Option value="MX">MX</Option>
              <Option value="TXT">TXT</Option>
              <Option value="SRV">SRV</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="name"
            label="记录名称"
            rules={[{ required: true, message: '请输入记录名称' }]}
          >
            <Input placeholder="例如: c2.example.com" />
          </Form.Item>
          <Form.Item
            name="value"
            label="记录值"
            rules={[{ required: true, message: '请输入记录值' }]}
          >
            <Input placeholder="例如: 192.168.1.100" />
          </Form.Item>
          <Form.Item
            name="ttl"
            label="TTL"
            rules={[{ required: true, message: '请输入TTL' }]}
          >
            <Input type="number" placeholder="例如: 300" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DnsC2;