"""
@copyright Mikko Tuohimaa 2018
"""

class NoSequenceFoundError(ValueError):
    pass

class WordPacker(object):
    def __init__(self, line_length=80):
        self.line_length = line_length

    def pack(self, text):
        dictionary = self.get_dictionary(text)
        return self.get_output_lines(dictionary, self.line_length)

    @staticmethod
    def get_dictionary(text):
        dictionary = {}
        for word in text.split():
            try:
                word_len = len(word)
                dictionary[word_len].append(word)
            except KeyError:
                dictionary[word_len] = [word]

        return dictionary

    @classmethod
    def get_output_lines(cls, dictionary, line_length):
        word_count_dict = {key: len(dictionary[key]) for key in dictionary}
        output_lines = []

        while dictionary:
            line_words = []
            line_remaining = line_length
            try:
                while line_remaining > 0:
                    keys = cls.get_keys(word_count_dict, max_length=line_remaining)
                    for key in keys:
                        word = dictionary[key].pop()
                        line_words.append(word)
                        line_remaining -= key + 1
                        if not dictionary[key]:
                            del dictionary[key]
                            del word_count_dict[key]
                        else:
                            word_count_dict[key] -= 1

            except ValueError:
                pass
            finally:
                output_lines.append(' '.join(line_words))

        return output_lines

    @staticmethod
    def get_keys(word_count_dict, max_length=80):
        """
        Input data structure:
        {
            <word length>: <word count>,
            ...
        }
        """
        def get_keys_recursive(word_count_dict, max_length=80):
            keys = sorted(filter(lambda x: x <= max_length, word_count_dict.keys()), reverse=True)
            try:
                keys_max = max(keys)
            except ValueError:
                raise NoSequenceFoundError("Empty dict")

            if max_length <= keys_max and max_length in keys:
                return [max_length]
            else:
                # Find a sequence of keys which add up to max_length
                for biggest_key in keys:
                    try:
                        word_count_dict_copy = {key: word_count_dict[key] for key in keys if key <= biggest_key}
                        if word_count_dict_copy[biggest_key] == 1:
                            del word_count_dict_copy[biggest_key]
                        else:
                            word_count_dict_copy[biggest_key] -= 1

                        return [biggest_key] + get_keys_recursive(word_count_dict_copy, max_length - biggest_key - 1)
                    except NoSequenceFoundError:
                        pass

            raise NoSequenceFoundError("Couldn't find a sequence")

        try:
            return get_keys_recursive(word_count_dict, max_length)
        except NoSequenceFoundError:
            return [max(filter(lambda k: k <= max_length, word_count_dict))]
