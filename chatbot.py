import guardrails as gd
import openai 
import os
class Chatbot(): 
    def __init__(self): 
        """Preprocessing embeddings.txt file to get all unique categories"""

        # Define the attributes for which you want to find unique categories
        attributes = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']

        # Read the content of the embeddings.txt file
        with open('embeddings.txt', 'r') as file:
            content = file.read()

        # Split content into individual product entries
        products = content.strip().split('\n\n')

        # Initialize dictionaries to store unique categories for each attribute
        unique_categories = {attr: set() for attr in attributes}

        # Process each product entry and extract unique categories
        for product in products:
            lines = product.strip().split('\n')
            product_data = {}
            for line in lines:
                key, value = line.split(' : ', 1)
                product_data[key] = value.strip()

            # Extract unique categories for each attribute
            for attr in attributes:
                if attr in product_data:
                    unique_categories[attr].add(product_data[attr])

        # Print the unique categories for each attribute
        self.unique_categories = unique_categories
        self.attributes = attributes
    
    def get_guardrail_instance(self, metadata = "", messages = ""): 
        category_string_to_attr = {attr : str() for attr in self.attributes}
        for attr in self.attributes : 
            unique_cat = self.unique_categories[attr]
            cat_string = "valid-choices : {["
            for cat in unique_cat: 
                cat_string += f"'{cat}', "
            cat_string = cat_string[:len(cat_string) - 2]
            cat_string += ']}'
            category_string_to_attr[attr] = cat_string
        
        messages = messages[:3] # only last 3 messages
        # for attr in category_string_to_attr.keys(): 
        #     print(attr, category_string_to_attr[attr])
        rail_spec = f"""
            <rail version = "0.1"> 
                <output> 
                    <string name = "response"
                        description = "Response to the user Query"
                    />
                    <string name = "gender" 
                        description = "Gender or sex of person identified through metadata or prompt"
                        format = "{category_string_to_attr['gender']}; multiple-matches"
                    />
                    <string name = "articleType" 
                        description = "Type of clothing article"
                        format = "{category_string_to_attr['articleType']}; multiple-matches"
                    />
                    <string name = "baseColour" 
                        description = "Colour of clothing article"
                    />
                </output>

                <prompt>
                    You are a prompt classifier who should extract information from the metadata of the user or the query itself. 
                    You can return multiple categories if you feel like they are similar enough.
                    In the response be friendly and helpful. Make sure to mention to mention to the user what exactly you inferred from their query.
                    If the user asks something unrelated to fashion then fill the response with the fallback message, don't respond with your own knowledge.  
                    FALLBACK MESSAGE: 
                    I am a fashion assistant. I am not able to help you regarding the above. Please ask something related. 
                    METADATA : 
                    {metadata}
                    USER QUERY: 
                    {{{{user_query}}}}
                    @complete_json_suffix_v2
                </prompt>
            </rail>
        """
        
        guard = gd.Guard.from_rail_string(rail_string=rail_spec)
        return guard
    
    def _make_openai_query(self, guard, messages): 
        """Makes the acutal open AI call, returns the vector DB queryable string"""
        import dotenv
        dotenv.load_dotenv()
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        raw_llm_output, validated_output = guard(
            openai.Completion.create, 
            engine = 'text-davinci-003', 
            max_tokens = 256, 
            prompt_params = {'user_query' : messages}, 
            temperature = 0.1
        )
        return validated_output
    
    def get_chatbot_reply(self, messages): 
        guard = self.get_guardrail_instance(messages = messages)
        return self._make_openai_query(guard, messages)

