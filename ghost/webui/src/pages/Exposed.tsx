import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Tag, Descriptions, Modal } from 'antd';
import { ReloadOutlined, EyeOutlined, CopyOutlined, DeleteOutlined } from '@ant-design/icons';


interface ExposedService {
  id: string;
  name: string;
  type: string;
  port: number;
  status: string;
  url: string;
  created: string;
  description: string;
}

const Exposed: React.FC = () => {
  const [services, setServices] = useState<ExposedService[]>([]);
  const [loading, setLoading] = useState(false);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedService, setSelectedService] = useState<ExposedService | null>(null);

  // 获取暴露的服务列表
  const fetchServices = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取暴露的服务列表
      // 暂时使用模拟数据
      const mockServices: ExposedService[] = [
        {
          id: '1',
          name: 'Web Server',
          type: 'HTTP',
          port: 8080,
          status: 'active',
          url: 'http://localhost:8080',
          created: '2026-03-31 09:00:00',
          description: '本地Web服务器'
        },
        {
          id: '2',
          name: 'API Service',
          type: 'HTTPS',
          port: 9090,
          status: 'active',
          url: 'https://localhost:9090',
          created: '2026-03-31 09:30:00',
          description: 'API服务'
        },
        {
          id: '3',
          name: 'Database',
          type: 'TCP',
          port: 3306,
          status: 'inactive',
          url: 'tcp://localhost:3306',
          created: '2026-03-31 10:00:00',
          description: '数据库服务'
        }
      ];
      setServices(mockServices);
      message.success('获取暴露服务列表成功');
    } catch (error) {
      console.error('Error fetching services:', error);
      message.error('获取暴露服务列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 复制URL到剪贴板
  const handleCopyUrl = (url: string) => {
    navigator.clipboard.writeText(url).then(() => {
      message.success('URL已复制到剪贴板');
    }).catch(err => {
      console.error('Error copying URL:', err);
      message.error('复制URL失败');
    });
  };

  // 查看服务详情
  const handleViewDetail = (service: ExposedService) => {
    setSelectedService(service);
    setDetailVisible(true);
  };

  // 删除服务
  const handleDelete = async (id: string) => {
    try {
      // 这里应该调用WebSocket服务删除服务
      setServices(services.filter(service => service.id !== id));
      message.success('删除服务成功');
    } catch (error) {
      console.error('Error deleting service:', error);
      message.error('删除服务失败');
    }
  };

  // 启动服务
  const handleStart = async (service: ExposedService) => {
    try {
      // 这里应该调用WebSocket服务启动服务
      setServices(services.map(s => 
        s.id === service.id ? { ...s, status: 'active' } : s
      ));
      message.success(`启动服务 ${service.name} 成功`);
    } catch (error) {
      console.error('Error starting service:', error);
      message.error('启动服务失败');
    }
  };

  // 停止服务
  const handleStop = async (service: ExposedService) => {
    try {
      // 这里应该调用WebSocket服务停止服务
      setServices(services.map(s => 
        s.id === service.id ? { ...s, status: 'inactive' } : s
      ));
      message.success(`停止服务 ${service.name} 成功`);
    } catch (error) {
      console.error('Error stopping service:', error);
      message.error('停止服务失败');
    }
  };

  useEffect(() => {
    fetchServices();
  }, []);

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
        <Tag color={type === 'HTTP' ? 'blue' : type === 'HTTPS' ? 'green' : 'orange'}>
          {type}
        </Tag>
      ),
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
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '活跃' : '非活跃'}
        </Tag>
      ),
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      render: (url: string) => (
        <Space>
          <a href={url} target="_blank" rel="noopener noreferrer">
            {url}
          </a>
          <Button 
            icon={<CopyOutlined />} 
            size="small" 
            onClick={() => handleCopyUrl(url)}
          />
        </Space>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created',
      key: 'created',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: ExposedService) => (
        <Space size="middle">
          <Button 
            icon={<EyeOutlined />} 
            size="small" 
            onClick={() => handleViewDetail(record)}
          >
            详情
          </Button>
          {record.status === 'inactive' ? (
            <Button 
              type="primary" 
              size="small" 
              onClick={() => handleStart(record)}
            >
              启动
            </Button>
          ) : (
            <Button 
              danger 
              size="small" 
              onClick={() => handleStop(record)}
            >
              停止
            </Button>
          )}
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
        title="暴露服务管理" 
        extra={
          <Button 
            icon={<ReloadOutlined />} 
            onClick={fetchServices}
            loading={loading}
          >
            刷新
          </Button>
        }
      >
        <Table 
          columns={columns} 
          dataSource={services} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="服务详情"
        open={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailVisible(false)}>
            关闭
          </Button>
        ]}
      >
        {selectedService && (
          <Descriptions bordered>
            <Descriptions.Item label="名称">{selectedService.name}</Descriptions.Item>
            <Descriptions.Item label="类型">{selectedService.type}</Descriptions.Item>
            <Descriptions.Item label="端口">{selectedService.port}</Descriptions.Item>
            <Descriptions.Item label="状态">
              <Tag color={selectedService.status === 'active' ? 'green' : 'red'}>
                {selectedService.status === 'active' ? '活跃' : '非活跃'}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="URL" span={2}>
              <a href={selectedService.url} target="_blank" rel="noopener noreferrer">
                {selectedService.url}
              </a>
            </Descriptions.Item>
            <Descriptions.Item label="创建时间">{selectedService.created}</Descriptions.Item>
            <Descriptions.Item label="描述" span={2}>
              {selectedService.description}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>
    </div>
  );
};

export default Exposed;