import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Modal, message, Spin } from 'antd';

const { Title } = Typography;

interface Module {
  id: string;
  name: string;
  category: string;
  description: string;
  author: string;
  version: string;
  status: 'installed' | 'available' | 'update';
}

const Modules: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [modules, setModules] = useState<Module[]>([]);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [selectedModule, setSelectedModule] = useState<Module | null>(null);

  // 模拟数据
  const mockModules: Module[] = [
    {
      id: '1',
      name: 'mimikatz',
      category: 'credentials',
      description: 'Windows credential harvesting tool',
      author: 'Benjamin Delpy',
      version: '2.2.0',
      status: 'installed',
    },
    {
      id: '2',
      name: 'meterpreter',
      category: 'exploit',
      description: 'Advanced payload for post-exploitation',
      author: 'Rapid7',
      version: '1.0.0',
      status: 'installed',
    },
    {
      id: '3',
      name: 'powershell',
      category: 'scripting',
      description: 'PowerShell execution module',
      author: 'Microsoft',
      version: '5.1',
      status: 'installed',
    },
    {
      id: '4',
      name: 'beacon',
      category: 'payload',
      description: 'Cobalt Strike beacon payload',
      author: 'Cobalt Strike',
      version: '4.5',
      status: 'available',
    },
  ];

  useEffect(() => {
    // 模拟加载数据
    setTimeout(() => {
      setModules(mockModules);
      setLoading(false);
    }, 1000);
  }, []);

  const handleModuleDetail = (module: Module) => {
    setSelectedModule(module);
    setDetailModalVisible(true);
  };

  const handleModuleInstall = (id: string) => {
    setModules(modules.map(module => 
      module.id === id ? { ...module, status: 'installed' } : module
    ));
    message.success('模块已安装');
  };

  const handleModuleUpdate = (id: string) => {
    setModules(modules.map(module => 
      module.id === id ? { ...module, status: 'installed' } : module
    ));
    message.success('模块已更新');
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类别',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => (
        <Tag color={category === 'credentials' ? 'blue' : category === 'exploit' ? 'red' : category === 'scripting' ? 'green' : 'purple'}>
          {category}
        </Tag>
      ),
    },
    {
      title: '版本',
      dataIndex: 'version',
      key: 'version',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = '';
        let text = '';
        switch (status) {
          case 'installed':
            color = 'green';
            text = '已安装';
            break;
          case 'available':
            color = 'blue';
            text = '可用';
            break;
          case 'update':
            color = 'orange';
            text = '可更新';
            break;
          default:
            color = 'default';
            text = status;
        }
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Module) => (
        <Space size="middle">
          <Button size="small" onClick={() => handleModuleDetail(record)}>
            详情
          </Button>
          {record.status === 'available' && (
            <Button type="primary" size="small" onClick={() => handleModuleInstall(record.id)}>
              安装
            </Button>
          )}
          {record.status === 'update' && (
            <Button type="primary" size="small" onClick={() => handleModuleUpdate(record.id)}>
              更新
            </Button>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>模块管理</Title>
      
      <Card>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={modules} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title={`模块详情: ${selectedModule?.name}`}
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>,
        ]}
        width={600}
      >
        {selectedModule && (
          <div>
            <p><strong>名称:</strong> {selectedModule.name}</p>
            <p><strong>类别:</strong> {selectedModule.category}</p>
            <p><strong>描述:</strong> {selectedModule.description}</p>
            <p><strong>作者:</strong> {selectedModule.author}</p>
            <p><strong>版本:</strong> {selectedModule.version}</p>
            <p><strong>状态:</strong> {selectedModule.status}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Modules;