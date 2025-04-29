'use client'
import React, { useEffect, useState } from "react";
import { Layout, Menu, theme } from "antd";
import type { MenuProps } from "antd";
import axios from './api/axios';
import GameContent from "./GameContent";

const { Header, Content, Sider } = Layout;

type Game = {
  id: number;
  title: string;
  genre: string;
  description?: string;
  img?: string;
};

const items1: MenuProps["items"] = ["1", "2", "3"].map((key) => ({
  key,
  label: `nav ${key}`,
}));

const Page: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [current, setCurrent] = useState<string>("");

  const onClick: MenuProps["onClick"] = (e) => {
    setCurrent(e.key); // key = id gry (string)
  };

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  useEffect(() => {
    axios.get('/games/')
      .then((res) => {
        setGames(res.data);
        console.log(res.data);
      })
      .catch((err) => console.error(err));
  }, []);

  type MenuItem = Required<MenuProps>["items"][number];

  const buildMenuItems = (games: Game[] = []): MenuItem[] => {
    if (!games.length) return [];

    const grouped = games.reduce((acc: Record<string, Game[]>, game) => {
      if (!acc[game.genre]) {
        acc[game.genre] = [];
      }
      acc[game.genre].push(game);
      return acc;
    }, {});

    return Object.entries(grouped).map(([genre, games]) => ({
      key: genre,
      label: genre,
      children: games.map((game) => ({
        key: game.id.toString(),   // <-- key to id gry
        label: game.title,
      })),
    }));
  };

  const items = buildMenuItems(games);
  const selectedGame = games.find((g) => g.id.toString() === current);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={["2"]}
          items={items1}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Layout>
        <Sider width={200} style={{ background: colorBgContainer }}>
          <Menu
            mode="inline"
            onClick={onClick}
            selectedKeys={[current]}
            defaultOpenKeys={["RPG", "MMO"]}
            style={{ height: "100%", borderRight: 0 }}
            items={items}
          />
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            {selectedGame ? (
              <GameContent game={selectedGame} />
            ) : (
              <div>Wybierz grę z listy.</div>
            )}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default Page;
