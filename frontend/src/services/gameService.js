import api from './api';

const getAll = () => {
  return api.get('/game');
}

const getById = (id) => {
  return api.get(`/game/${id}`)
}

const getMostPopular = (params) => {
  return api.get('/games/most-popular', {
    params: params
  })
}

const search = (query) => {
  return api.get(`/game?$text=${query}`);
}

export default {
  getAll,
  getById,
  getMostPopular,
  search
}
