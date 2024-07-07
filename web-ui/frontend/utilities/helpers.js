import { PostProcessorsData } from '../data/data'
import { getTextFromLLM, getResults } from '../apis/axios'



export function getPostProcessorsDictionary () {
    return PostProcessorsData.reduce((acc, { key, id }) => {
        acc[key] = document.getElementById(id).checked 
        return acc
    }, {});
}


// function markInputPII (pii_response) {
//     let inpQues = document.getElementById("input-question")
//     let text = inpQues.value

//     let out = pii_response



function markInputPII (pii_response) {
    // console.log('marking pii')
    // console.log(pii_response)
    let inpQues = document.getElementById("input-question")
    // takes the input text and wraps all the appaearances of anything with <> in mark tag
    var text = inpQues.value
        
    let out = pii_response

    // let out = "My name is <personal_name> and I am a <personal_profession> at <personal_company>"
    // let out = text;
    let in_arr = text.split(/([\s\r\n!.,?]+)/)
    let out_arr = out.split(/([\s\r\n!.,?]+)/)
    // console.log(in_arr)
    // console.log(out_arr)
    let j = 0;
    // declare array of size of out_arr
    let in_arr_copy = out_arr
    for (let i = 0; i < out_arr.length; i++) {
        // if (out_arr[i].startsWith('<') && (out_arr[i].endsWith('>') || out_arr[i][out_arr[i].length - 2] == '>')) { 
        if (out_arr[i].startsWith('<') && (out_arr[i].endsWith('>'))) { 
            
            let temp = ''
            // let j = i
            
            if (i==out_arr.length-1) {
                console.log(11111111)
                while (j<in_arr.length-1) {
                    temp += in_arr[j]
                    j++
                }
                temp += in_arr[j]

                in_arr_copy[i] = '<mark class="marked">' + temp + '</mark>'
                break
            }
            else {

                if (i<out_arr.length-1) {
                    console.log(1)
                    while (j<in_arr.length-1 && in_arr[j+1]!=out_arr[i+1]) {
                        temp += in_arr[j]
                        j++
                    }
                    temp += in_arr[j]

                    // console.log(temp)
                    // console.log(in_arr[j+1])
                    // if (['.', ',', '?', '!'].indexOf(in_arr[j+1]) == -1) {
                    //     temp += in_arr[j+1]
                    // }

                    in_arr_copy[i] = '<mark class="marked">' + temp + '</mark>'
                }

            }
        }

        j++;
    }

    text = in_arr_copy.join('')

    text = text
        .replace(/\n/g, '<br>')
        .replace(/\r/g, '<br>');


    console.log(text)
    document.getElementsByClassName('backdrop')[0].innerHTML = text
    
    var ua = window.navigator.userAgent.toLowerCase();
    var isIE = !!ua.match(/msie|trident\/7|edge/);
}


export function generateText (inputQuestion, setUnfilteredOutput, setFilteredOutput, setShowLoadingBars, selectedLlm, setShowProcessingText, setErrorText, setSendButtonDisableStatus) {
    setFilteredOutput('')
    setUnfilteredOutput('')
    setErrorText('')
    setSendButtonDisableStatus(true)
    setShowProcessingText(true)
    // setShowLoadingBars([true, true])

    const postProcessorsDictionary = getPostProcessorsDictionary()

    // console.log('hereeeeeeee')

    // Sends the input question into detectors
    getResults(inputQuestion, postProcessorsDictionary)
    .then((response) => {
        // When no violation is detected in input question
        setShowProcessingText(false)
        setSendButtonDisableStatus(false)

        if (!response.verdict.length) {

            setShowLoadingBars([true, false])

            // Sends the input question into LLM and gets the output
            getTextFromLLM(inputQuestion, selectedLlm)
            .then((response) => {
                setUnfilteredOutput(response)
                // setShowLoadingBars([true, false])
                setShowLoadingBars([false, true])
            
                // Sends the output from LLM into detectors
                getResults(response, postProcessorsDictionary)
                .then((response2) => {
                    setShowLoadingBars([false, false])
                    setSendButtonDisableStatus(false)
                    if (response2.verdict.length) {
                        setFilteredOutput(`The generated text contains ${response2.verdict.join(', ')}.`)
                    }
                    else {
                        setFilteredOutput(`The generated text does not viloate any selected detectors.`)
                    }
                    // setProcessingText('')
                })
                .catch((error) => {
                    // setProcessingText('')
                    setFilteredOutput(error.response.data)
                    setShowLoadingBars([false, false])
                    setSendButtonDisableStatus(false)
                })
            
            })
            .catch((error) => {
                // setShowProcessingText(false)
                setErrorText('')
                setUnfilteredOutput(error.response.data)
                // setFilteredOutput({'error' : {'message': 'Error in getting response from LLM'}})
                setShowLoadingBars([false, false])
            })
        }

        // If verdict is not empty, then violation was detected in input question
        else {
            setSendButtonDisableStatus(true)
            setErrorText(`The entered text contains ${response.verdict.join(', ')}. Please remove it and try again.`)

            if (response.verdict.includes('personally identifiable information')) {
                console.log(response.pii_response.message)
                markInputPII(response.pii_response.message)
            }
            setShowProcessingText(false)
            setUnfilteredOutput('')
            // setFilteredOutput({'error' : {'message': 'The entered text contains personal information. Please remove it and try again'}})
            setFilteredOutput('')
            setShowLoadingBars([false, false])
        }
    })
}



export function updateSendButtonStatus(selectedLlm, inputQuestion, setButtonDisableStatus, setButtonTitle) {
    // console.log(selectedLlm, inputQuestion)
    if (inputQuestion == '') {
        setButtonDisableStatus(true)
        if (selectedLlm == '') {
            setButtonTitle('Please select an LLM')
        }
        else{
            setButtonTitle('Please enter an input question')
        }
    }

    else {
        setButtonDisableStatus(false)
    }

    return
}