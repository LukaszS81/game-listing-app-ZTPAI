'use client'
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Breadcrumb, Layout, Menu } from 'antd';

const { Header, Content, Sider } = Layout;

// Typ danych dla gry
type Game = {
  id: number;
  title: string;
  genre: string;
  description?: string;
  img?: string;
};

const items1: MenuProps['items'] = ['1', '2', '3'].map((key) => ({
  key,
  label: `nav ${key}`,
}));

const items2: MenuProps['items'] = [UserOutlined, LaptopOutlined, NotificationOutlined].map(
  (icon, index) => {
    const key = String(index + 1);
    return {
      key: `sub${key}`,
      icon: React.createElement(icon),
      label: `subnav ${key}`,
      children: Array.from({ length: 4 }).map((_, j) => {
        const subKey = index * 4 + j + 1;
        return {
          key: subKey,
          label: `option${subKey}`,
        };
      }),
    };
  },
);

const HomePage: React.FC = () => {
  const [genres, setGenres] = useState<Game[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [rpg, setRpg] = useState<Game[]>([]);
  const [mmo, setMmo] = useState<Game[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/games/')
      .then(res => {
        setGenres(res.data); // Przypisanie danych do stanu genres
        // Rozdzielenie gier na RPG i MMO
        setRpg(res.data.filter((game: Game) => game.genre === 'RPG'));
        setMmo(res.data.filter((game: Game) => game.genre === 'MMO'));
      })
      .catch(err => console.error(err));
    setLoaded(true);
  }, []);

  // Sprawdzanie w konsoli
  if (loaded) {
    console.log(rpg); // Gry RPG
    console.log(mmo); // Gry MMO
  }

  return (
    <Layout style={{ height: '100%' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
          items={items1}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Layout>
        <Sider width={200} style={{}}>
          <Menu
            mode="inline"
            defaultSelectedKeys={['1']}
            defaultOpenKeys={['sub1']}
            style={{ height: '100%', borderRight: 0 }}
          >
            {/* Dodanie gatunków RPG i MMO do menu */}
            <Menu.SubMenu key="RPG" title="RPG">
              {rpg.map((game) => (
                <Menu.Item key={game.id}>{game.title}</Menu.Item>
              ))}
            </Menu.SubMenu>
            <Menu.SubMenu key="MMO" title="MMO">
              {mmo.map((game) => (
                <Menu.Item key={game.id}>{game.title}</Menu.Item>
              ))}
            </Menu.SubMenu>
          </Menu>
        </Sider>
        <Layout style={{ padding: '0 24px 24px' }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
            }}
          >
            Content
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default HomePage;
