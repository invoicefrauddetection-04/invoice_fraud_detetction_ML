from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():

    embedding_model = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2",

        model_kwargs={

            "device": "cpu"

        },

        encode_kwargs={

            "normalize_embeddings": True

        }

    )

    return embedding_model


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    model = get_embedding_model()

    vector = model.embed_query(

        "Duplicate invoice fraud"

    )

    print("=" * 60)

    print("Embedding Dimension :", len(vector))

    print("=" * 60)

    print(vector[:10])