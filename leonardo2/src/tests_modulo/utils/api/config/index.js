import apiFetcher from '@/tests_modulo/utils/api/fetchFromApi'

export async function getAvailableDomains() {
  try {
    const res = await apiFetcher.get('/config/domains')
    return res.data
  } catch (err) {
    console.log('Error submiting config for test generation', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}
