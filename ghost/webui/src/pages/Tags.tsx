import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Form, Input, Modal, message, Spin, Popconfirm } from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
} from '@ant-design/icons';

const { Title } = Typography;

interface TagItem {
  id: string;
  name: string;
  color: string;
  description: string;
  count: number;
}

const Tags: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [tags, setTags] = useState<TagItem[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTag, setEditingTag] = useState<TagItem | null>(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockTags: TagItem[] = [
    {
      id: '1',
      name: 'important',
      color: '#f5222d',
      description: '重要目标',
      count: 5,
    },
    {
      id: '2',
      name: 'web',
      color: '#1890ff',
      description: 'Web服务器',
      count: 10,
    },
    {
      id: '3',
      name: 'database',
      color: '#52c41a',
      description: '数据库服务器',
      count: 3,
    },
    {
      id: '4',
      name: 'windows',
      color: '#faad14',
      description: 'Windows系统',
      count: 8,
    },
  ];

  useEffect(() => {
    // 模拟加载数据
    setTimeout(() => {
      setTags(mockTags);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAddTag = () => {
    setEditingTag(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditTag = (tag: TagItem) => {
    setEditingTag(tag);
    form.setFieldsValue(tag);
    setModalVisible(true);
  };

  const handleSaveTag = () => {
    form.validateFields().then(values => {
      if (editingTag) {
        // 编辑现有标签
        setTags(tags.map(tag => 
          tag.id === editingTag.id ? { ...tag, ...values } : tag
        ));
        message.success('标签已更新');
      } else {
        // 添加新标签
        const newTag: TagItem = {
          id: (tags.length + 1).toString(),
          ...values,
          count: 0,
        };
        setTags([...tags, newTag]);
        message.success('标签已添加');
      }
      setModalVisible(false);
    });
  };

  const handleDeleteTag = (id: string) => {
    setTags(tags.filter(tag => tag.id !== id));
    message.success('标签已删除');
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: TagItem) => (
        <Tag color={record.color} style={{ fontSize: 14, padding: '4px 8px' }}>
          {name}
        </Tag>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '使用次数',
      dataIndex: 'count',
      key: 'count',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: TagItem) => (
        <Space size="middle">
          <Button size="small" onClick={() => handleEditTag(record)}>
            <EditOutlined />
          </Button>
          <Popconfirm
            title="确定要删除此标签吗？"
            onConfirm={() => handleDeleteTag(record.id)}
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
      <Title level={2}>标签管理</Title>
      
      <Card>
        <div style={{ marginBottom: 16, textAlign: 'right' }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddTag}>
            添加标签
          </Button>
        </div>
        
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={tags} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title={editingTag ? "编辑标签" : "添加标签"}
        open={modalVisible}
        onOk={handleSaveTag}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入标签名称' }]}
          >
            <Input placeholder="标签名称" />
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入标签描述' }]}
          >
            <Input placeholder="标签描述" />
          </Form.Item>
          <Form.Item
            name="color"
            label="颜色"
            rules={[{ required: true, message: '请选择标签颜色' }]}
          >
            <Input type="color" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Tags;