<template>
  <div class="main-box">
    <div class="info-box">
      <div class="metadata-box">
        <UserForm @form-submitted="handleChildData" />
      </div>
      <div class="chat-box" ref="scrollableDiv">
        <div v-if="conversation_history.length === 0">
          <h1 style="color: #ffdd00; text-align: center; padding-top: 22%">
            Your conversation with Flipbot will appear here
          </h1>
        </div>
            <div v-for="prompt in conversation_history" :key="prompt" class="conversation">
              <div v-if="prompt.role === 'user'" class="checkbox-user">
                <p>YOU</p>
                <div class="user-chat">
                  {{ prompt.content }}
                </div>
              </div>
              <div v-else class="checkbox-gpt">
                <p>FLIPBOT</p>
                <div class="gpt-chat">{{ prompt.content }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="product-box">
          <div class="history">
            <div v-if="products.length === 0" class="if-zero">
              <h1 style="color: #ffdd00; text-align: left"><u>
                Welcome to FLIPBOT
              </u>
                <br/>
                <br/>
              </h1>
              <h1 style="color: #ffdd00; text-align: left">
                Start a chat with Flipbot below to see products you'll love!
                <br /><br />Please provide your details on the left before you begin, ensuring an accurate fashion outfit suggestion.
                <br /><br />Feel free to upload an image, and we'll use it to identify similar outfits for you.<br /><br />Happy Shopping !!!
              </h1>
            </div>
            <div class="allProducts">
              <ProductCard v-for="(product, index) in this.products" :key="index" :url="product" />
          </div>
        </div>
        <div class="text-box">
          <div>
            <textarea placeholder="Start the conversation here!!!" class="chatbox-input" v-model="prompt" />
        </div>
        <div><button type="submit" @click="sendPrompt">Submit</button></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProductCard from "./ProductCard.vue";
import UserForm from "./UserForm.vue";
export default {
  name: "MetaData",
  submit: "Submit",
  components: {
    UserForm,
    ProductCard,
  },
  data() {
    return {
      prompt: "",
      count: 0,
      conversation_history: [],
      products: [],
      location: "",
      productCount: 1,
      age: 1,
      gender: "",
      similarity: 0.5,
    };
  },
  methods: {
    handleChildData(formData) {
      this.location = formData.location;
      this.productCount = formData.productCount;
      this.age = formData.age;
      this.similarity = formData.similarity;
      this.gender = formData.gender;
    },

    async sendPrompt() {
      this.products = [];
      //update conv history 
      this.conversation_history.push({ "role": "user", "content": this.prompt });
      this.prompt = "";
      //object as per API docs
      let data = {
        'metadata': {
          'age': this.age,
          'gender': this.gender,
          'similarity': parseFloat(this.similarity),
          'location': this.location,
          'k': parseInt(this.productCount)
        },
        'messages': this.conversation_history
      }

      //making the actual axios post request
      axios.post("http://127.0.0.1:5000/", data)
        .then((response) => {
          console.log(response)
          //incase of resolution of promise
          let assistant_message = response.data['message'];

          //update personal history
          this.conversation_history.push({  
            'role': 'gpt',
            'content': assistant_message
          })

          //set products to all image urls
          let image_urls = response.data['image_urls']
          console.log('Matched images : ', image_urls)
          this.products = image_urls
        })
        .catch((error) => {
          console.log(error)
          this.conversation_history.push({
            'role': 'gpt',
            'content': `There has been an error : {${error}}`

          })
        })
    },

    scrollToEnd() {
      const scrollableDiv = this.$refs.scrollableDiv;
      scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
    },
  },
};
</script>

<style>
.allProducts {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-items: center;
  justify-content: space-evenly;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: #e0e0e0 #f0f0f0;
}

.allProducts::-webkit-scrollbar {
  width: 6px;
  background-color: grey;
}

.allProducts::-webkit-scrollbar-thumb {
  background-color: white;
  border-radius: 3px;
}

.allProducts::-webkit-scrollbar-thumb:hover {
  background-color: white;
}

.main-box {
  width: 100%;
  height: 96vh;
  display: flex;
}

.text-box {
  display: flex;
  align-items: center;
  justify-content: space-around;
  box-sizing: border-box;
  margin-bottom: 1vh;
}

.checkbox-user {
  margin-left: auto;
}

.checkbox-gpt {
  margin-right: auto;
}

.info-box {
  width: 55vh;
  height: 93%;
  margin: 1.5rem 1.5rem 1.5rem 1.5rem;
  border-radius: 10px;
  border: 5px solid silver;
  color: white;
  display: flex;
  flex-direction: column;
}

.conversation {
  display: flex;
  flex-direction: row;
  height: auto;
  width: 55vh;
  padding: 10px;
}

.user-chat {
  margin-left: auto;
  padding: 2vh 2vh 2vh 2vh;
  border-radius: 10px;
  margin-right: 2.5vh;
  background-color: #ffdd00;
  color: black;
}

.gpt-chat {
  margin-left: auto;
  padding: 2vh 2vh 2vh 2vh;
  border-radius: 10px;
  background-color: #f7a200;
  color: black;
}

.product-box {
  display: flex;
  flex-direction: column;
  width: 65%;
  height: 93%;
  margin: 1.5rem 1.5rem 1.5rem 1.5rem;
  border-radius: 10px;
  border: 5px solid silver;
}

.chat-box {
  width: 100%;
  height: 50%;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: #e0e0e0 #f0f0f0;
}

.chat-box::-webkit-scrollbar {
  width: 6px;
  background-color: grey;
}

.chat-box::-webkit-scrollbar-thumb {
  background-color: white;
  border-radius: 3px;
}

.chat-box::-webkit-scrollbar-thumb:hover {
  background-color: white;
}

.metadata-box {
  width: 100%;
  height: 60%;
}

.chatbox-input {
  width: 110vh;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  resize: horizontal;
  font-family: "Roboto", sans-serif;
}

button {
  padding: 10px 20px;
  background-color: #ffdd00;
  color: black;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.chatbox-input::placeholder {
  font-family: "Roboto", sans-serif;
}

.history {
  width: 95%;
  height: 95%;
  margin: 2.5% 2.5% 2.5% 2.5%;
  overflow-y: hidden;
}
</style>
