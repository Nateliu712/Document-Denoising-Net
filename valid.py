require 'torch'
require 'xlua'

# functions

def valid():

	# set model to evaluate mode
	model:evaluate()

	valid_cleaned_data = torch.Tensor(valid_data:size(1), test_data:size(2), test_data:size(3))

	# test over test data
	print('==> validating on test set:')
	valid_nrow = valid_data:size(1)
	for t = 1,valid_nrow do

		# disp progress
		xlua.progress(t, valid_nrow)

		# get new sample
		input = valid_data[{{t},}]
		input = input:cuda()

		# valid sample
		pred = thresholding:forward(model:forward(input))
		valid_cleaned_data[{{t,}}] = pred:float()

	path.mkdir(opt.path_saveimg)
	valid_cleaned_images_pred = patch2img(valid_cleaned_data, valid_images)
	for i = 1,#valid_cleaned_images_pred do
		image.save("save/valid_cleaned_images_" .. i .. ".png", valid_cleaned_images_pred[i])

	valid_score = calc_rsme(valid_cleaned_images, valid_cleaned_images_pred)
	print("valid_score: " .. string.format("%.5f", valid_score))
