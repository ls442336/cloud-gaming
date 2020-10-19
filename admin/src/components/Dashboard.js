import React, { useState, useEffect } from "react";
import { Grid, Box, Card, Typography, makeStyles } from '@material-ui/core';
import DataCard from './DataCard'
import Chart from "react-google-charts"
import api from '../api'
import moment from 'moment'

const useStyles = makeStyles({
  root: {
    flexGrow: 1,
  }
});


export const Dashboard = () => {
  const [sessionCount, setSessionCount] = useState(0)
  const [userCount, setUserCount] = useState(0)
  const [instanceCount, setInstanceCount] = useState(0)
  const [lastSessions, setLastSessions] = useState([[0, 0]])
  const [popularGames, setPopularGames] = useState([[0, 0]])
  const classes = useStyles();

  useEffect(() => {
    api.get('/session', {
      params: {
        '$count': true,
        'active': true
      }
    }).then(res => {
      setSessionCount(res.data)
    })

    api.get('/instance', {
      params: {
        '$count': true,
        'active': true
      }
    }).then(res => {
      setInstanceCount(res.data)
    })

    api.get('/user', {
      params: {
        '$count': true,
        'active': true
      }
    }).then(res => {
      setUserCount(res.data)
    })

    api.get('/sessions/last-dates', {
      params: {
        'days': 30,
        'limit': 100
      }
    }).then(res => {
      const data = res.data

      const dates = data.map(date => moment(date).format('DD/MM/YYYY'))

      let today = moment()
      let sessions = []

      for (let i = 0; i < 30; i++) {
        sessions.push([today.format("DD/MM"), dates.filter(date => date == today.format("DD/MM/YYYY")).length])
        today = today.subtract(1, 'days')
      }

      sessions = sessions.reverse()

      setLastSessions(sessions)
    })

    api.get('/games/most-popular', {
      params: {
        'limit': 5
      }
    }).then(res => {
      const data = res.data

      const games = data.map(game => [game.game ? game.game.name : 'Sem nome', game.count])

      console.log(games)

      setPopularGames(games)
    });

  }, [])

  return (
    <div className={classes.root}>
      <Card style={{ padding: 25 }}>
        <Typography variant="h6" style={{ marginBottom: 25 }}>
          Bem-vindo à Área do Administrador
        </Typography>
        <Grid container direction="row" spacing={3} alignItems="center">
          <Grid item xs={9}>
            <Box border={1} borderColor={'#BAC9D0'}>
              <Chart
                width={'100%'}
                height={'400px'}
                chartType="LineChart"
                loader={<div style={{ textAlign: 'center' }}>Carregando gráfico...</div>}
                data={[
                  ['x', 'Sessões'],
                  ...lastSessions
                ]}
                options={{
                  title: 'Número de Sessões por Dia (Últimos 30 dias)',
                  hAxis: {
                    title: 'Dias Atrás',
                  },
                  vAxis: {
                    title: 'Número de sessões',
                  },
                }}
                rootProps={{ 'data-testid': '1' }}
              />
            </Box>
          </Grid>
          <Grid item xs={3}>
            <Grid container direction="column" spacing={3}>
              <Grid item xs><DataCard title={sessionCount} description="sessões ativas" color="#BAC9D0" /></Grid>
              <Grid item xs><DataCard title={instanceCount} description="instâncias registradas" color="#BAC9D0" /></Grid>
              <Grid item xs><DataCard title={userCount} description="usuários conectados" color="#BAC9D0" /></Grid>
            </Grid>
          </Grid>
        </Grid>
        <Grid container direction="row" style={{ marginTop: 25 }}>
          <Grid item xs={12}>
            <Box border={1} borderColor={'#BAC9D0'} style={{ padding: 25 }}>
              <Chart
                width={'100%'}
                height={'400px'}
                chartType="Bar"
                loader={<div style={{ textAlign: 'center' }}>Carregando gráfico...</div>}
                data={[
                  ['Nome do Jogo', 'Jogado'],
                  ...popularGames
                ]}
                options={{
                  chart: {
                    title: 'Jogos Mais Populares',
                    subtitle: 'Os 5 jogos mais jogados no momento',
                  }
                }}
                rootProps={{ 'data-testid': '2' }}
              />
            </Box>
          </Grid>
        </Grid>
      </Card>
    </div>
  );
}