import axios from 'axios'


export async function getResults (inputText, postProcessors) {
    let baseURL =  'http://127.0.0.1:8000/'
    // console.log(inputText, postProcessors)
    
    let response = await axios.post(`${baseURL}postprocessing/`,
                                    {'input_text':inputText, 'config': postProcessors})

    // console.log(response.data)

    return response.data
}

export async function getTextFromLLM (inputText, selectedLlm) {
    let baseURL =  'http://127.0.0.1:8000/'

    // console.log(1111111111111111111111111)
    // console.log(inputText, selectedLlm)

    let response = await axios.get(`${baseURL}postprocessing/`,
                                    {params: {'input_text':inputText, 'llm': selectedLlm }})

    return response.data
}


export async function getInputPII (inputText) {
    let baseURL =  'http://127.0.0.1:8000/'

    let response = await axios.post(`${baseURL}anonymize_text/`,
                                    {'input_text':inputText})
    console.log(response.data)
    return response.data
}