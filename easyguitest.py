import easygui
answer = easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
print(answer)
answer = easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
print(answer)