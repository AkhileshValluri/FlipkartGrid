<template>
    <div class="main-box">
        <div class = "metadata-box">This is MetaBox</div>
        <div class = "chat-box">
            <div class="history"></div>
            <div><textarea placeholder="Start the conversation here!!!" class="chatbox-input"/></div>
        </div>
    </div>
</template>

<script>
    export default{
        name : 'MetaData',
    }
</script>

<style>
    .main-box{
        width:95rem;
        height:46rem;
        display: flex;  
    }

    .metadata-box{
        width:30%;
        height:93%;
        margin: 1.5rem 1.5rem 1.5rem 1.5rem;
        border-radius: 2.5%;
        border: 5px solid silver;
    }

    .chat-box{
        display: flex;
        flex-direction: column;
        
        width: 65%;
        height:93%;
        margin: 1.5rem 1.5rem 1.5rem 1.5rem;
        border-radius: 2.5%;
        border: 5px solid silver;
    }

    .chatbox-input{
        width: 95%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        box-sizing: border-box;
        margin: 1vh 1vh 3vh 3vh;
    }

    .history{
        width: 95%;
        height: 95%;
        margin: 2.5% 2.5% 2.5% 2.5%;
    }

    .chatbox-input:focus {
        border-color: #007bff;
        outline: none;
    }
</style>