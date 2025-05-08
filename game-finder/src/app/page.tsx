'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Layout, Menu, theme, Button } from 'antd'
import type { MenuProps } from 'antd'
import axios from './api/axios'
import GameContent from './GameContent'

const { Header, Content, Sider } = Layout

type Game = {
  id: number
  title: string
  genre: string
  description?: string
  img?: string
}

const Page: React.FC = () => {
  const router = useRouter()
  const [games, setGames] = useState<Game[]>([])
  const [current, setCurrent] = useState<string>('')

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token')
      if (!token) {
        router.push('/login')
      }
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  const onClick: MenuProps['onClick'] = (e) => {
    setCurrent(e.key)
  }

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()

  useEffect(() => {
    axios
      .get('/games/')
      .then((res) => {
        setGames(res.data)
      })
      .catch((err) => {
        console.error('Błąd pobierania gier:', err)
      })
  }, [])

  const buildMenuItems = (games: Game[] = []) => {
    const grouped = games.reduce((acc: Record<string, Game[]>, game) => {
      if (!acc[game.genre]) acc[game.genre] = []
      acc[game.genre].push(game)
      return acc
    }, {})

    return Object.entries(grouped).map(([genre, games]) => ({
      key: genre,
      label: genre,
      children: games.map((game) => ({
        key: game.id.toString(),
        label: game.title,
      })),
    }))
  }

  const items = buildMenuItems(games)
  const selectedGame = games.find((g) => g.id.toString() === current)

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']} items={[]} style={{ flex: 1 }} />
        <Button type="primary" onClick={handleLogout}>
          Wyloguj
        </Button>
      </Header>
      <Layout>
        <Sider width={200} style={{ background: colorBgContainer }}>
          <Menu
            mode="inline"
            onClick={onClick}
            selectedKeys={[current]}
            style={{ height: '100%', borderRight: 0 }}
            items={items}
          />
        </Sider>
        <Layout style={{ padding: '0 24px 24px' }}>
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
  )
}

export default Page
