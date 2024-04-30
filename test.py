import repl


if __name__ == "__main__":
    # query = "Adjustment of DNA"
    # query = "Scandinavian wild carnivore animal"
    query = "Cold climate cat"
    print("Query:", query)
    repl.rag(query, number_of_documents=1)


