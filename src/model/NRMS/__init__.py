import torch
from model.NRMS.news_encoder import NewsEncoder
from model.NRMS.user_encoder import UserEncoder
from model.general.click_predictor import ClickPredictor


class NRMS(torch.nn.Module):
    """
    NRMS network.
    Input a candidate news and a list of user clicked news, produce the click probability.
    """

    def __init__(self, config, pretrained_word_embedding=None):
        super(NRMS, self).__init__()
        self.config = config
        self.news_encoder = NewsEncoder(config, pretrained_word_embedding)
        self.user_encoder = UserEncoder(config)
        self.click_predictor = ClickPredictor()

    def forward(self, candidate_news, clicked_news):
        """
        Args:
          candidate_news: Tensor(batch_size) * num_words_title,
          clicked_news:
            [Tensor(batch_size) * num_words_title] * num_clicked_news_a_user
        Returns:
          click_probability: batch_size
        """
        # batch_size, word_embedding_dim
        candidate_news_vector = self.news_encoder(candidate_news)
        # batch_size, num_clicked_news_a_user, word_embedding_dim
        clicked_news_vector = torch.stack(
            [self.news_encoder(x) for x in clicked_news], dim=1)
        # batch_size, word_embedding_dim
        user_vector = self.user_encoder(clicked_news_vector)
        # batch_size
        click_probability = self.click_predictor(candidate_news_vector,
                                                 user_vector)
        return click_probability