import apiFetcher from '@/utils/api/fetchFromApi'

export async function getOne(id) {
  try {
    const res = await apiFetcher.get(`/evaluation/${id}`)
    return res.data
  } catch (err) {
    console.log('Error fetching test', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}


export async function getOneEval(id) {
  try {
    const res = await apiFetcher.get(`/evaluation/individualResult/${id}`)
    return res.data
  } catch (err) {
    console.log('Error fetching test', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function submit(test) {
  try {
    console.log('sending')
    console.log(test)
    const res = await apiFetcher.post(`/evaluation`, test)
    return res.data
  } catch (err) {
    console.log('Error submiting solution', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}
