## StarSpace

StarSpace is a general-purpose neural model for efficient learning of entity embeddings for solving a wide variety of problems:

- Learning word, sentence or document level embeddings.
- Information retrieval: ranking of sets of entities/documents or objects, e.g. ranking web documents.
- Text classification, or any other labeling task.
- Metric/similarity learning, e.g. learning sentence or document similarity.
- Content-based or Collaborative filtering-based Recommendation, e.g. recommending music or videos.
- Embedding graphs, e.g. multi-relational graphs such as Freebase.
- NEW Image classification, ranking or retrieval (e.g. by using existing ResNet features).


In the general case, it learns to represent objects of different types into a common vectorial embedding space, hence the star ('*', wildcard) and space in the name, and in that space compares them against each other. It learns to rank a set of entities/documents or objects given a query entity/document or object, which is not necessarily the same type as the items in the set.

See the [paper](https://arxiv.org/abs/1709.03856) for more details on how it works.


## News

- New license and patents: now StarSpace is under BSD license. Checkout [LICENSE](https://github.com/facebookresearch/StarSpace/blob/master/LICENSE.md) and [PATENTS](https://github.com/facebookresearch/StarSpace/blob/master/PATENTS) for details.
- We added support for real-valued input and label weights: checkout the [File Format](https://github.com/facebookresearch/StarSpace/#file-format) and [ImageSpace](https://github.com/facebookresearch/StarSpace/#imagespace-learning-image-and-label-embeddings) section for more details on how to use weights in input and label.





## Requirements

StarSpace builds on modern Mac OS and Linux distributions. Since it uses C++11 features, it requires a compiler with good C++11 support. These include :

(gcc-4.6.3 or newer) or (clang-3.3 or newer)
Compilation is carried out using a Makefile, so you will need to have a working make.

You need to install Boost library and specify the path of boost library in makefile in order to run StarSpace. Basically:

    $wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.zip
    $unzip boost_1_63_0.zip
    $sudo mv boost_1_63_0 /usr/local/bi


Optional: if one wishes to run the unit tests in src directory, google test is required and its path needs to be specified in 'TEST_INCLUDES' in the makefile.