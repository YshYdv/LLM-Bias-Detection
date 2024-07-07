import React, { useEffect, useState } from 'react'
// import getResults, { getInputPII, getTextFromLLM } from '../apis/axios'
import { PostProcessorsData, LlmsList } from '../data/data'
import SkeletonLoader from "tiny-skeleton-loader-react"
import { RiSendPlane2Fill } from "react-icons/ri";
import { generateText, updateSendButtonStatus, getPostProcessorsDictionary } from '../utilities/helpers'
import { BiSolidError, BiMessageCheck } from 'react-icons/bi'

const loadingBars = () => {
    return (
        <div className='output-loading-bars'>
            <SkeletonLoader background='gray' width='90%' height={16} circle={false} radius={2}/>
            <SkeletonLoader background='gray' width='50%' height={16} circle={false} radius={2}/>
            <SkeletonLoader background='gray' width='90%' height={16} circle={false} radius={2}/>
            <SkeletonLoader background='gray' width='50%' height={16} circle={false} radius={2}/>
        </div>

    )
}



export default function MainSection() {

    let [selectedLlm, setSelectedLlm] = useState('')
    let [inputQuestion, setInputQuestion] = useState('')
    let [postProcessorChange, setPostProcessorChange] = useState(true)


    let [sendButtonDisableStatus, setSendButtonDisableStatus] = useState(true)
    let [buttonTitle, setButtonTitle] = useState('')

    let [unfilteredOutput , setUnfilteredOutput] = useState('')
    let [filteredOutput , setFilteredOutput] = useState('')
    let [showLoadingBars, setShowLoadingBars] = useState([false, false])


    let [showProcessingText, setShowProcessingText] = useState(false)
    let [errorText, setErrorText] = useState('')
 

    const handleLlmDivClick = (id) => {
        LlmsList.map((llm) =>{
            if (llm.id === id) {
                const element = document.getElementById(llm.id);
                element.className = 'llm-option-button-selected';
            } else {
                const element = document.getElementById(llm.id);
                element.className = 'llm-option-button';
            }
          })
    };



    useEffect(() => {
        // Increases the text area on changing input as per need
        const textarea = document.getElementById("input-question");
        textarea.style.height = "18px"
        textarea.style.height = `${textarea.scrollHeight}px`
    }, [inputQuestion])


    useEffect(() => {
        if (inputQuestion == '') {
            setSendButtonDisableStatus(true)
            setButtonTitle('Please enter a question')
        }
        else if (selectedLlm == '') {
            setSendButtonDisableStatus(true)
            setButtonTitle('Please select a LLM')
        }
        else {
            let postProcessorsList = []
            PostProcessorsData.map((postProcessor) => {
                if (document.getElementById(postProcessor.id).checked) {
                    postProcessorsList.push(postProcessor.key)
                }
            })
            if (postProcessorsList.length == 0) {
                setSendButtonDisableStatus(true)
                setButtonTitle('Please select at least one post processor')
            }
            else {
                setSendButtonDisableStatus(false)
                setButtonTitle('')
            }
        }

        document.getElementsByClassName('backdrop')[0].innerHTML = ''
    }, [inputQuestion, selectedLlm, postProcessorChange])

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    return (
        <div className='main-body'>
            <div className="input-section">

                <div className='llm-selection-bar'>
                    {
                        LlmsList.map((llm) => (
                            <button className='llm-option-button' id={llm.id} 
                                    onClick={() => {
                                        // console.log(selectedLlm)
                                                    setSelectedLlm(llm.key)
                                                    sleep(10000)
                                                    handleLlmDivClick(llm.id)
                                                    // console.log(selectedLlm)
                                                    // updateSendButtonStatus(selectedLlm, inputQuestion, setSendButtonDisableStatus, setButtonTitle)
                                                    }}>
                                {llm.labelName}
                            </button>
                        ))
                    }
                </div>

                <div className='text-input-section'>
                    <div className="text-container">
                        <div className="backdrop">
                            {/* <div class="highlights"></div> */}
                        </div>
                        <textarea id="input-question" className='text-input-section-textarea' 
                            name="input"
                            placeholder="Send a message..." 
                                onChange={() => {
                                // console.log(document.getElementById("input-question").value)
                                // setInputQuestionFunction(setInputQuestion)
                                setInputQuestion(document.getElementById("input-question").value)
                                // console.log(inputQuestion)
                                // updateSendButtonStatus(selectedLlm, inputQuestion, setSendButtonDisableStatus, setButtonTitle)
                            }}
                            ></textarea>
                    </div>

                    <button className='input-send-button'
                    title={buttonTitle}
                    disabled={sendButtonDisableStatus}
                            onClick={() => {
                                // setInputQuestionFunction(inputQuestion, setInputQuestion)
                                generateText(inputQuestion ,setUnfilteredOutput ,setFilteredOutput ,setShowLoadingBars, selectedLlm, setShowProcessingText, setErrorText, setSendButtonDisableStatus)
                            }}>
                        {
                            showProcessingText ? (
                                <div class="spinner-border" role="status"></div>
                            ) : (
                                <RiSendPlane2Fill className='send-button-icon'/>
                            )
                        }
                    </button>

                </div>

                <div className='processing-n-error-section'>
                    {/* {
                        !showProcessingText ? (null) : (
                            <div className='processing-n-error-box' id="processing">
                                <div className='processing-box'>
                                    <div class="spinner-border" role="status"></div>
                                    Processing...
                                </div>
                            </div> 
                        )
                    } */}

                    {
                        errorText == '' ? (null) : (
                            <div className='processing-n-error-box' id="error">
                                <div class="alert alert-danger alert-danger-input-changes" role="alert">
                                    <BiSolidError className='error-icon'/>
                                    {errorText}
                                </div>
                            </div> 
                        )
                    }
                </div>

                <div className="post-processor-selection-box">
                    <div className='post-processors-list'>
                        {
                            PostProcessorsData.map((postProcessor) => (
                                <div className='post-processor-list-item'>
                                    <input type="checkbox" id={postProcessor.id}
                                            onClick={ () => {
                                                setPostProcessorChange(!postProcessorChange)
                                            }}/>
                                    <span>{postProcessor.labelName}</span>
                                </div>
                            ))
                        }
                    </div>
                </div>
            </div>
            

            <div className='output-section'>
                <div className='output-box' id="raw-output">
                    <div className='output-box-heading'>
                        Original Response
                    </div>

                    <div className='output-box-response'>
                        {
                            showLoadingBars[0] ? (
                                <div>
                                    {loadingBars()}
                                </div>
                            ) : (
                                <div>
                                    {unfilteredOutput}
                                </div>
                            )
                        }
                    </div>
                </div>

                <div className='output-box' id="filtered-output">
                    <div className='output-box-heading'>
                        Response with Guardrails
                    </div>

                    <div className='output-box-response'>
                        {
                            showLoadingBars[1] ? (
                                <div>
                                    {loadingBars()}
                                </div>
                            ) : (
                                // <div>
                                //     {
                                //         Object.entries(filteredOutput).map(([key, output]) => (
                                //             <div className='output-text'>   
                                //                 {/* {`${output.message}`} */}
                                //                 {/* {output.message.split(/\n/).map(line => <div key={line}>{line}<br /></div>)} */}
                                //                 <br />
                                //             </div>
                                //         ))
                                //     }
                                // </div>
                                <div>
                                    {
                                        filteredOutput == 'The generated text does not viloate any selected detectors.' ? (
                                            <div class="alert alert-success alert-success-output-changes" role="alert">
                                                <BiMessageCheck className='check-icon'/>
                                                {filteredOutput}
                                            </div>
                                        ) : 
                                            filteredOutput == '' ? (null) : (
                                                // {filteredOutput}
                                                <div class="alert alert-danger alert-danger-output-changes" role="alert">
                                                    <BiSolidError className='error-icon'/>
                                                    {filteredOutput}
                                                </div>
                                            )
                                        
                                        //     <div class="alert alert-danger alert-danger-output-changes" role="alert">
                                        //         <BiSolidError className='error-icon'/>
                                        //         {filteredOutput}
                                        //     </div>
                                        // )
                                    }
                                </div>
                            )
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}