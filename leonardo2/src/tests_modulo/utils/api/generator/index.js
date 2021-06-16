import apiFetcher from '@/tests_modulo/utils/api/fetchFromApi'

export async function generateNew(id, config, editing) {
  try {
    const url = editing ? '/generator/new?editing=true' : '/generator/new'
    const res = await apiFetcher.post(url, {
      id,
      config
    })
    return res.data
  } catch (err) {
    console.log('Error submiting config for test generation', err?.response)
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}

export async function replaceQuestions(replace, test) {
  try {
    const res = await apiFetcher.post('/generator/edit', {
      replace,
      test
    })
    return res.data
  } catch (err) {
    console.log(
      'Error submiting config for question replacement',
      err?.response
    )
    throw new Error(err?.response?.data || 'UNKNOWN')
  }
}
