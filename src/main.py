import post_generation
import hashtag_algorithm

def main(user_idea):
    # Execute the post generation process
    post_generation.main(user_idea)
    
    # Execute the hashtag generation process
    hashtag_algorithm.main()

if __name__ == "__main__":
    # Example usage
    user_idea = (
        "We are conducting a gen ai hackathon + work shop in our college. were we will be teach the how to create a full stack webapplication using only gen ai and later we will be conducting a hackathon where the students will be creating a web application using gen ai. The best web application will be having a chance to attend the mubai tech fest."
    )
    main(user_idea)
