<template>
  <div class="main-box">
    <div class="info-box">
      <div class="metadata-box">
        <UserForm @form-submitted="handleChildData" />
      </div>
      <div class="chat-box" ref="scrollableDiv">
        <div v-if="conversation_history.length === 0">
          <h1 style="color: yellowgreen; text-align: center; padding-top: 22%">
            Your conversation with Flipbot will appear here
          </h1>
        </div>
        <div
          v-for="prompt in conversation_history"
          :key="prompt"
          class="conversation"
        >
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
          <h1 style="color: yellowgreen; text-align: center">
            Welcome to Flipbot !!!
          </h1>
          <h1 style="color: yellowgreen; text-align: center">
            There are no products to display, start chatting with the flipbot in
            the textbox below to display products that you like !!!
            <br /><br />Before you start, please enter all your details in the
            left so that we can give you an accurate fashion outfit.
            <br /><br />You can also give us an image so that we can find out
            outfits that are similar to it. <br /><br />Happy Shopping !!!
          </h1>
        </div>
        <div class="allProducts">
          <ProductCard
            v-for="product in products"
            :key="product"
            :url="getImageUrl(product)"
          />
        </div>
      </div>
      <div class="text-box">
        <div>
          <textarea
            placeholder="Start the conversation here!!!"
            class="chatbox-input"
            v-model="prompt"
          />
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
      // TODO Send prompt data to backend
      console.log(this.prompt);
      console.log(
        this.location,
        this.productCount,
        this.age,
        this.gender,
        this.similarity
      );
      try {
        const response = await axios.get("URL_OF_BACKEND");
        this.products = response.data;
      } catch (error) {
        console.error("Error fetching images:", error);
      }

      this.conversation_history.push({ role: "user", content: this.prompt });
      this.conversation_history.push({
        role: "gpt",
        content: "hello" /* GPT PROMPT TO BE ADDED */,
      });
      this.$nextTick(() => {
        this.scrollToEnd();
      });
    },

    getImageUrl(imageName) {
      return `../../../../matches/${imageName}`; // Replace with your image directory path
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
  width: 95rem;
  height: 46rem;
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
  background-color: yellowgreen;
}

.gpt-chat {
  margin-left: auto;
  padding: 2vh 2vh 2vh 2vh;
  border-radius: 10px;
  background-color: crimson;
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
  height: 48vh;
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
  height: 50%;
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
  background-color: #007bff;
  color: #fff;
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
