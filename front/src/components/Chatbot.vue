<template>
    <div class="container m-auto p-1">
        <div class="card mx-auto">
            <div class="card-header bg-transparent">
                <div class="navbar navbar-expand p-0">
                    <h5>Chatbot</h5>
                    <!-- close button -->
                    <ul class="navbar-nav ms-auto" v-if="chatBotState">
                        <li class="nav-item">
                            <a class="btn btn-secondary nav-link text-light" @click="closeBot">
                                <i class="bx bx-x bx-md"></i>
                            </a>
                        </li>
                    </ul>
                    <ul class="navbar-nav ms-auto" v-else>
                        <li class="nav-item">
                            <a class="btn btn-secondary nav-link text-light" @click="$router.go(-1)">
                                Back
                            </a>
                        </li>
                    </ul>
                    <!-- header close button-->

                </div>
            </div>
            <div class="card-body p-2" style="height: 400px; overflow: auto;" ref="messagesContainer">

                <div class="d-flex align-items-baseline mb-4">

                    <div class="position-relative avatar">
                        <img src="https://s.yimg.com/ny/api/res/1.2/zWHycYRsBKQ6xwdBGQtw4g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTU0MDtjZj13ZWJw/https://s.yimg.com/os/creatr-uploaded-images/2023-12/5f7be670-943f-11ee-af7f-41b7060d20ba"
                            class="img-fluid" style="border-radius: 50%; height:100%;" alt="">
                        <span
                            class="position-absolute bottom-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </div>

                    <div class="pe-2">
                        <div>
                            <div class="card card-text d-inline-block p-2 px-3 m-1" v-if="chatBotState">Hi! Here's the summary of this lecture.
                            </div>
                            <div class="card card-text d-inline-block p-2 px-3 m-1" v-else>
                                Hi! How may i assist you today ?
                            </div>
                        </div>
                        
                    </div>
                </div>

            <div class="messages-container">
              <div v-for="(msg, index) in messages" :key="index" :class="{'justify-content-end': msg.role === 'user', 'justify-content-start': msg.role !== 'user'}" class="d-flex align-items-baseline mb-4">
                <div v-if="msg.role === 'user' && msg.type !== 'summary'"  class="d-flex">
                <div class="pe-2">
                  <div>
                    <div class="card card-text d-inline-block p-2 px-3 m-1" v-if="msg.parts && msg.type === 'text'" v-html="msg.parts.text"></div>
                    <span v-if="msg.parts && msg.type === 'file'" class="text-end">
                        <i class='bx bx-file bx-lg'></i>
                    </span><br>
                    <span class="card card-text d-inline-block p-2 px-3 m-1" v-if="msg.parts && msg.type === 'file'">{{msg.name}}</span>
                  </div>
                </div>

                <div>
                    <div class="position-relative avatar">
                        <i class="bx bx-user bx-md"></i>
                        <span
                            class="position-absolute bottom-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </div>

                  </div>
                </div>
            
                <div v-else class="d-flex">
                   <div v-if="msg.type!='file' && msg.type!='summary'"> 
                    <div>
                    <div class="position-relative avatar">
                        <img src="https://s.yimg.com/ny/api/res/1.2/zWHycYRsBKQ6xwdBGQtw4g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTU0MDtjZj13ZWJw/https://s.yimg.com/os/creatr-uploaded-images/2023-12/5f7be670-943f-11ee-af7f-41b7060d20ba"
                            class="img-fluid" style="border-radius: 50%; height:100%;" alt="">
                        <span
                            class="position-absolute bottom-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </div>

                  </div>

                <div class="pe-2">
                  <div>
                    <div class="card card-text d-inline-block p-2 px-3 m-1" v-if="msg.parts.text" v-html="msg.parts.text"></div>
                  </div>
                </div>
            </div> 
            </div>


            </div>
          </div>
            </div>
        


             <!-- card-body end -->
            <div class="m-5"></div>

            <div class="card-footer bg-white position-absolute w-100 bottom-0 m-0 p-1">
                <div class="input-group">
                    <div class="input-group-text bg-transparent border-0">
                        <input ref="fileInput" type="file" style="display: none;" @change="onFileChange">
                        <button class="btn btn-light text-secondary" @click="triggerFileUpload"> 
                            <i class="bx bx-paperclip bx-sm"></i>
                        </button>
                    </div>
                    <input type="text" v-model="message" class="form-control border-0" placeholder="Write a message..." @keyup.enter="sendMessage(message,'user','text')">
                    <div class="input-group-text bg-transparent border-0" >
                        <button @click="sendMessage(message,'user','text')" class="btn btn-light text-secondary">
                            <i class="bx bx-send bx-sm"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>

import { GoogleGenerativeAI } from "@google/generative-ai";
import DOMPurify from 'dompurify';
import { marked } from 'marked';

// Fetch your API_KEY
const API_KEY = "AIzaSyByHZtQ1cLVH8lGVuJzeIZAuSaMuIsqffg";
// Reminder: This should only be for local testing

// Access your API key (see "Set up your API key" above)
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash"});


export default {
  name: 'Chatbot',
  props: {
    chatBotState: {
      type: String,
      required: false,
      default:null,
    },
    clearHistory:{
        type: Boolean,
        required:false,
        default:false,
    },
  },
  data() {
    return {
      message:'',
      messages:[],
      //for streaming chat
      loading: true,
      //formattedMessage: '',
      tempChunk: '',
    }
  },
  
  mounted() {
    if (this.chatBotState) {

      //this.messages.push({ parts : { text : this.chatBotState}, role: 'model', type:'text', name:'' } );

      this.sendMessage(this.chatBotState,'user','summary');

      console.log(this.messages);

      //const { GoogleGenerativeAI } = await import('@google/generative-ai');
      //console.log(GoogleGenerativeAI);
    }
  
  },
  computed: {
    filteredMessages() {
      // Determine the starting index based on chatBotState
      const startIndex = this.chatBotState ? 1 : 0;
      return this.messages.slice(startIndex);
    }
  },

  watch: {

    messages() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },

    clearHistory(newValue, oldValue) {
      // This function is called whenever `selectedVideoUrl` changes
      this.messages=[];
      //console.log("messages[]="+this.messages);
      this.clearHistory=false;
    },
    chatBotState(newValue, oldValue) {
      // This function is called whenever `chatBotState` changes
      
        //console.log("chatBotState changed messages[]="+this.messages);
      this.sendMessage(this.chatBotState,'user','summary');
      
    },
  },
  methods: {

    //for processing streaming
    appendDataChunk(dataChunk) {
          this.tempChunk += dataChunk;
          this.processTempChunk();
    },
    // for processing streaming
    processTempChunk(flag) {
      // Check for end markers to decide if chunk is complete
      const chunkEndPattern = /\n{2,}/; // Two or more newlines
      if (chunkEndPattern.test(this.tempChunk)) {
        const splitChunks = this.tempChunk.split(chunkEndPattern);
        const completeChunks = splitChunks.slice(0, -1);
        this.tempChunk = splitChunks.slice(-1)[0]; // Keep the remaining incomplete chunk

        completeChunks.forEach(chunk => {
          
          this.messages[this.messages.length - 1].parts.text += marked(chunk);
          this.$nextTick(() => {
          this.scrollToBottom();
        });
          
        });
      }

      if (flag) {

        this.messages[this.messages.length - 1].parts.text += marked(this.tempChunk);
        this.tempChunk = ''; // Clear tempChunk after appending

        this.$nextTick(() => {
          this.scrollToBottom();
        });

                
      
    }

  },

    scrollToBottom() {
      
      const container = this.$refs.messagesContainer;
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
      });

    },

    async onFileChange(event) {
      const file = event.target.files[0];
      if (file && file.type === 'application/pdf') {
        const formData = new FormData();
        formData.append('file', file);

        try {
          const response = await fetch('http://127.0.0.1:5000/api/PDFtoText', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error('Network response was not ok');
          }

          const data = await response.json();
          this.sendMessage(data.text,'user','file',file.name);


        } catch (error) {
          console.log('There was a problem with the fetch operation:', error);
          this.sendMessage('Sorry! upload failed, try again.','model','text');
        }
      } else {
        alert('Please select a PDF file.');
      }
    },

    triggerFileUpload() {
      //console.log("file upload triggered")
      this.$refs.fileInput.click();
    },

    stripHtmlTagsWithDompurify(htmlString) {
          const cleanHtml = DOMPurify.sanitize(htmlString, { ALLOWED_TAGS: [] });
          return cleanHtml;
        },


    async sendMessage(text, role, type, name) {
      if (text.trim()) {

        this.messages.push({ parts : { text : text }, role: role, type: type, name: name });  // add the message with sender information to the array
        this.message = '';  // clear the input field after sending the message        

        this.$nextTick(() => {
          this.scrollToBottom();
        });

        const jsonBody = this.prepareJsonBody(this.messages);
        //console.log(JSON.stringify(jsonBody));
        const body = {'contents' : jsonBody, 'stream':true};
        //console.log(body);

        //const prompt = "Write a story about a magic backpack."

        const chat = await model.startChat({history:jsonBody});


        const result = await chat.sendMessageStream(text);

        //console.dir(result);

        let received = '';
        this.messages.push({ parts : { text: "" }, role: 'model', type:'text'});
        for await (const chunk of result.stream) {

          this.appendDataChunk(chunk.text());
          const chunkText = chunk.text();
          //console.log(chunkText);
          received += chunkText;
        

        }
        this.processTempChunk(true);


      }
    }, 

    prepareJsonBody(messages) {
      // Map the messages array to the required JSON structure
      return messages.filter(msg => msg.parts && msg.parts.text).map(msg => ({
        parts: [{ text: msg.parts.text} ],
        role: msg.role,
      }));
    },

    receiveMessage(text,role,type,name) {
      if (text.trim()) {
        this.messages.push({ parts : { text: text }, role: 'model', type:type, name:''});  // add the message from the other user to the array
        console.log(this.messages);
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    closeBot(){
        this.$emit('closeChatBot');
    },

    
    
    
  }
}
</script>


<style>
    a.nav-link {
        color: gray;
        font-size: 18px;
        padding: 0;
    }

    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid #b09a95;
        padding: 2px;
        flex: none;
    }

    input:focus {
        outline: 0px !important;
        box-shadow: none !important;
    }

    
</style>