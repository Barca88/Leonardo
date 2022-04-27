import apiFetcher from '@/utils/api/fetchFromApi'

export async function getResultStats() {
  try {
    const res = await apiFetcher.get('/stats')
    return res.data
  } catch (err) {
    console.log('Error fetching stats', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}
