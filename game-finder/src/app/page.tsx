'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Layout, Menu, theme, Button, message } from 'antd'
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
  const [isAdmin, setIsAdmin] = useState(false)

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()

  // Sprawdzanie tokena, pobieranie gier i roli admina
  useEffect(() => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      router.push('/login')
      return
    }

    // Pobierz listę gier
    axios
      .get('/games/')
      .then((res) => {
        setGames(res.data)
      })
      .catch((err) => {
        console.error('Błąd pobierania gier:', err)
      })

    // Sprawdź, czy user jest adminem
    axios
      .get('/user-info/', {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setIsAdmin(res.data.is_staff)
      })
      .catch((err) => console.error('Błąd pobierania user-info:', err))
  }, [router])

  // Kliknięcie w menu
  const onClick: MenuProps['onClick'] = (e) => {
    setCurrent(e.key)
  }

  // Wylogowanie
  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  // Buduj drzewo gatunków i gier
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

  // Obsługa przycisku "Dodaj grę"
  const handleAddGame = () => {
    // Zamiast sztywnego POST-a — przekierowanie do strony dodawania gry:
    router.push('/add-game')
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']} items={[]} style={{ flex: 1 }} />

        <div style={{ display: 'flex', gap: 8 }}>
          {/* Przycisk "Dodaj grę" tylko dla admina */}
          {isAdmin && (
            <Button type="primary" onClick={handleAddGame}>
              Dodaj grę
            </Button>
          )}
          <Button type="primary" onClick={handleLogout}>
            Wyloguj
          </Button>
        </div>
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
