import apiFetcher from '@/utils/api/fetchFromApi'

export async function getAll() {
  try {
    const res = await apiFetcher.get('/tests')
    return res.data
  } catch (err) {
    console.log('Error fetching tests', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function getAllPersonal() {
  try {
    const res = await apiFetcher.get('/tests/personal/$this.{$store.state.user.studentNumber}')
    return res.data
  } catch (err) {
    console.log('Error fetching tests', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}


export async function getAllActive() {
  try {
    
    const res = await apiFetcher.get('/tests/actives')
    return res.data
  } catch (err) {
    console.log('Error fetching tests', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function getNearFuture() {
  try {
    const res = await apiFetcher.get('/tests/nextTests')
    return res.data
  } catch (err) {
    console.log('Error fetching tests', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function getOne(id) {
  try {
    const res = await apiFetcher.get(`/tests/${id}`)
    return res.data
  } catch (err) {
    console.log('Error fetching tests', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function saveTest(test) {
  try {
    const res = await apiFetcher.put(`/tests/${test.id}`, test)
    return res.data
  } catch (err) {
    console.log('Error saving test', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function deleteOne(id) {
  try {
    const res = await apiFetcher.delete(`/tests/${id}`)
    return res.data
  } catch (err) {
    console.log('Error saving test', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}
