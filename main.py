


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')
    from sdv.single_table import GaussianCopulaSynthesizer
    from sdv.sampling import Condition

    saved_location = r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Pickle_file_locations\Engagement_Default_values_pickle_file\Engagement_Default_values_pickle_file.pkl'

    saved_location = r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Pickle_file_locations\Engagement_Default_values_pickle_file\Engagement_Default_values_pickle_file.pkl'
    synthesizer = GaussianCopulaSynthesizer.load(
        filepath=saved_location
    )

    synthetic_data = synthesizer.sample(num_rows=100)
    print(synthetic_data)
    # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
