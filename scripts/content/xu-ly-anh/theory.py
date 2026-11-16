"""Map source questions to topics; full responses live in theory_answers.py."""

BANK_MAP = dict(zip([f'1.{i}' for i in range(1,15)], ['color','cmy','hsv','raster','halftone','print-gray','diffusion','brightness','equalize','window','noise','indirect','edge-noise','why-compress']))
BANK_MAP.update(dict(zip([f'2.{i}' for i in range(1,17)], ['mix','rgb-cmy','raster','filters','derivative','kernels','canny','background','triangle','split','kmeans','knn','hopfield','kohonen','rlc','jpeg-dct'])))
UYEN_THEORY_MAP = {**BANK_MAP, '1.11':'noise', '1.12':'edge'}
CHAPTER_MAP = {
 3:['brightness','equalize','window','noise','filters','background','triangle','thresholds','restoration'],
 4:['mix','color','cmyk','hsv','raster','halftone','diffusion','color-tf'],
 5:['edge','derivative','kernels','laplace','canny','smooth','otsu','background','split'],
 6:['rlc','jpeg-dct','lzw','redundancy','huffman','compression','coder','jpeg','compression-tf'],
 7:['morphology','erode-dilate','open-close','clean','boundary','fill','component','morph-tf'],
}
