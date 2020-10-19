import React from 'react';
import { Admin, Resource, fetchUtils } from 'react-admin';
import { SessionList } from './resources/Session'
import { GameList, GameCreate, GameTitle, GameEdit } from './resources/Game'
import { Dashboard } from './components/Dashboard'
import restHapiProvider from './restHapiProvider'
import { InstanceList, InstanceTitle } from './resources/Instance'
import { UserList, UserTitle } from './resources/User'
import polyglotI18nProvider from 'ra-i18n-polyglot';
import portugueseMessages from 'ra-language-pt-br'
import authProvider from './authProvider'
import { createMuiTheme } from '@material-ui/core/styles';
import SportsEsports from '@material-ui/icons/SportsEsports'
import Storage from '@material-ui/icons/Storage'
import Person from '@material-ui/icons/Person'
import CastConnected from '@material-ui/icons/CastConnected'
import './App.css';

const i18nProvider = polyglotI18nProvider(() => portugueseMessages, 'ptbr');

// Adiciona o token durante as requisições
const httpClient = (url, options = {}) => {
  if (!options.headers) {
    options.headers = new Headers({ Accept: 'application/json' });
  }
  const token = localStorage.getItem('token');
  options.headers.set('Authorization', `Bearer ${token}`);
  return fetchUtils.fetchJson(url, options);
}

const dataProvider = restHapiProvider(process.env.REACT_APP_API_URL, httpClient);

const theme = createMuiTheme({
  palette: {
    primary: { main: '#000000' },
    secondary: { main: '#263238' },
    contrastThreshold: 3,
    tonalOffset: 0.2,
  }
})
function App() {
  return (
    <Admin theme={theme} locale="ptbr" i18nProvider={i18nProvider} dashboard={Dashboard} dataProvider={dataProvider} authProvider={authProvider}>
      <Resource name="session" list={SessionList} icon={CastConnected}/>
      <Resource name="game" list={GameList} create={GameCreate} title={GameTitle} edit={GameEdit} icon={SportsEsports} />
      <Resource name="instance" list={InstanceList} title={InstanceTitle} icon={Storage}/>
      <Resource name="user" list={UserList} title={UserTitle} icon={Person} />
    </Admin>
  );
}

export default App;