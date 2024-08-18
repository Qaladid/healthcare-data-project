if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Transform the data by standardizing text case and removing duplicates.
    
    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Transformed DataFrame with standardized text and no duplicates.
    """
    # Ensure the necessary columns exist before applying transformations
    if 'Name' in data.columns:
        # Standardize text to title case
        data['Name'] = data['Name'].str.title()  # Replace 'Name' with your actual column name

    # Remove duplicate rows based on all columns
    data = data.drop_duplicates()

    return data

@test
def test_output(output, *args) -> None:
    """
    Test the output of the transformation block.
    """
    assert output is not None, 'The output is undefined'
    assert 'Name' in output.columns, 'Expected column "Name" not found in the output'
    # Add more assertions if needed to verify the transformation
