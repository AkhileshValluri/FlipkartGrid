<template>
    <div class="main-box">
        <div class="info-box">
            <div class = "metadata-box">This is Metadata box</div>
            <div class ="chat-box">
                <div v-for="prompt in conversation_history" :key="prompt" class="conversation">
                    <div v-if="prompt.role === 'user'" class="checkbox-user">
                        <div class="user-chat">{{ prompt.content }}</div>
                    </div>
                    <div v-else class="checkbox-gpt">
                        <div class="gpt-chat">{{ prompt.content }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class = "product-box">
            <div class="history"></div>
            <div class="text-box">
                <div><textarea placeholder="Start the conversation here!!!" class="chatbox-input" v-model = "prompt"/></div>
                <div><button type="submit" @click="sendPrompt">Submit</button></div>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name : 'MetaData',
        data(){
            return{
                prompt: '',
                conversation_history: []
            }
        },
        methods : {
            sendPrompt(){
                // TODO Send prompt data to backend
                console.log(this.prompt)
                this.conversation_history.push({'role':'gpt', 'content':this.prompt})
            }
        }
    }
</script>

<style>
    .main-box{
        width:95rem;
        height:46rem;
        display: flex;  
    }

    .text-box{
        display: flex;
        align-items: center;
        justify-content: space-around;
        box-sizing: border-box;
        margin-bottom: 1vh;
    }

    .checkbox-user{
        margin-left: auto;
    }

    .checkbox-gpt{
        margin-right: auto;
    }

    .info-box{
        width:55vh;
        height:93%;
        margin: 1.5rem 1.5rem 1.5rem 1.5rem;
        border-radius: 10px;
        border: 5px solid silver;
        color: white;
        display: flex;
        flex-direction: column;

    }

    .conversation{
        display: flex;
        flex-direction: row;
        height: auto;
        width: 55vh;
        padding: 10px;
    }

    .user-chat{
        margin-left: auto;
        padding: 2vh 2vh 2vh 2vh;
        border-radius: 10px;
        margin-right: 2.5vh;
        background-color: yellowgreen;
    }

    .gpt-chat{
        margin-left: auto;
        padding: 2vh 2vh 2vh 2vh;
        border-radius: 10px;
        background-color: crimson;
    }

    .product-box{
        display: flex;
        flex-direction: column;
        width: 65%;
        height:93%;
        margin: 1.5rem 1.5rem 1.5rem 1.5rem;
        border-radius: 10px;
        border: 5px solid silver;
    }
    
    .chat-box{
        width: 100%;
        height: 48vh;
        overflow-y:auto;
        overflow-x: hidden;
    }

    .metadata-box{
        width: 100%;
        height: 50%;
        border: 1px solid silver;
    }

    .chatbox-input{
        width: 110vh;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        box-sizing: border-box;
        resize: horizontal;
        box-sizing: border-box;
        font-family:  'Roboto', sans-serif;
        resize: none;
    }

    button{
        padding: 10px 20px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }

    .chatbox-input::placeholder {
        font-family:  'Roboto', sans-serif;
    }

    .history{
        width: 95%;
        height: 95%;
        margin: 2.5% 2.5% 2.5% 2.5%;
    }
</style>